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
            # Path to the rmssd.txt file in the static directory
            file_path = os.path.join(settings.BASE_DIR, 'static', 'rmssd.txt')

            if not os.path.isfile(file_path):
                return Response(
                    {"detail": "RMSSD file not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Read RMSSD values from the file
            with open(file_path, 'r') as file:
                rmssd_values = [float(line.strip()) for line in file if line.strip()]

            print("Received RMSSD values:", rmssd_values)

            if not rmssd_values:
                return Response(
                    {"detail": "No RMSSD values available in the file."},
                    status=status.HTTP_412_PRECONDITION_FAILED,
                )

            # Generate the graph and get its file path
            graph_file_path = PlotGraph(rmssd_values)
            print(f"Generated graph at: {graph_file_path}")

            if not os.path.isfile(graph_file_path):
                return Response(
                    {"detail": "Graph file was not generated correctly."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Read the graph file and serve as a response
            with open(graph_file_path, 'rb') as graph_file:
                graph_data = graph_file.read()

            # Delete the graph file after sending the response
            try:
                os.remove(graph_file_path)
                print(f"Deleted graph file: {graph_file_path}")
            except Exception as delete_error:
                print(f"Error deleting graph file: {delete_error}")

            # Clear the contents of rmssd.txt after processing
            try:
                with open(file_path, 'w') as file:
                    file.truncate(0)
                print(f"Cleared contents of RMSSD file: {file_path}")
            except Exception as clear_error:
                print(f"Error clearing RMSSD file: {clear_error}")

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

