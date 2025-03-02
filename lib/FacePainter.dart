import 'package:flutter/material.dart';
import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';

class FacePainter extends CustomPainter {
  final List<Face> faces;
  final Size imageSize;

  FacePainter({required this.faces, required this.imageSize});

  @override
  void paint(Canvas canvas, Size size) {
    // Calculate the aspect ratio offsets to correctly map coordinates
    final double scaleX = size.width / imageSize.width;
    final double scaleY = size.height / imageSize.height;

    // Use the minimum scale to preserve the aspect ratio
    final double scale = scaleX < scaleY ? scaleX : scaleY;

    // Offset to center the bounding boxes if aspect ratio causes empty space
    final double offsetX = (size.width - imageSize.width * scale) / 2;
    final double offsetY = (size.height - imageSize.height * scale) / 2;

    // Define a red paint for the rectangle
    final Paint paint = Paint()
      ..color = Colors.red.withOpacity(0.5) // Semi-transparent red
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    for (Face face in faces) {
      // Get the bounding box of the face
      final Rect boundingBox = face.boundingBox;

      // Scale and position the bounding box correctly on the canvas
      final Rect scaledBox = Rect.fromLTRB(
        boundingBox.left * scale + offsetX,
        boundingBox.top * scale + offsetY,
        boundingBox.right * scale + offsetX,
        boundingBox.bottom * scale + offsetY,
      );

      // Draw the rectangle
      canvas.drawRect(scaledBox, paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
