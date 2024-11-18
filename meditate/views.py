from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
from .graph import PlotGraph
import os
from django.contrib.staticfiles import finders


@method_decorator(csrf_exempt, name='dispatch')
class Say(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({'message': 'Hello, world!'}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class GenerateHRVReport(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # Get RMSSD values from settings
            rmssd_values = settings.RMSSD
            print("Received RMSSD values:", rmssd_values)

            if not rmssd_values:
                return Response(
                    {"detail": "No RMSSD values available."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Generate the graph and get its file path
            graph_file_path = PlotGraph(rmssd_values)
            print(f"Generated graph at: {graph_file_path}")

            if not os.path.isfile(graph_file_path):
                return Response(
                    {"detail": "Graph file was not generated correctly."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Read the file and serve as a response
            with open(graph_file_path, 'rb') as graph_file:
                graph_data = graph_file.read()

            # Delete the file after sending the response
            try:
                os.remove(graph_file_path)
                print(f"Deleted graph file: {graph_file_path}")
            except Exception as delete_error:
                print(f"Error deleting file: {delete_error}")

            # Return the graph data with appropriate headers
            response = HttpResponse(
                graph_data, content_type="image/png"
            )
            response['Content-Disposition'] = 'inline; filename="hrv_report.png"'
            return response

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {"detail": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
