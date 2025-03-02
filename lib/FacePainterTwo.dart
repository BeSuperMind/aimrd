// import 'package:flutter/material.dart';
// import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';

// class FacePainter extends CustomPainter {
//   Face face;
//   final Size imageSize;

//   FacePainter({required this.face, required this.imageSize});

//   @override
//   void paint(Canvas canvas, Size size) {
//     // Define a red paint for the rectangle
//     final Paint paint = Paint()
//       ..color = Colors.red.withOpacity(0.5) // Semi-transparent red
//       ..style = PaintingStyle.stroke
//       ..strokeWidth = 2.0;

//     // Get the bounding box of the face
//     final Rect boundingBox = face.boundingBox;

//     // Scale and position the bounding box correctly on the canvas
//     final Rect scaledBox = Rect.fromLTRB(
//       boundingBox.left,
//       boundingBox.top,
//       boundingBox.right,
//       boundingBox.bottom,
//     );

//     // Draw the rectangle
//     canvas.drawRect(scaledBox, paint);
//   }

//   @override
//   bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
// }

import 'package:flutter/material.dart';
import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';

class FacePainter extends CustomPainter {
  final Face face; // Only drawing the first face
  final Size imageSize;

  FacePainter({required this.face, required this.imageSize});

  @override
  void paint(Canvas canvas, Size size) {
    // Calculate the scale factors to map face coordinates correctly
    final double scaleX = size.width / imageSize.width;
    final double scaleY = size.height / imageSize.height;

    // Use minimum scale to maintain aspect ratio
    final double scale = scaleX < scaleY ? scaleX : scaleY;

    // Offset to center the face box if aspect ratio causes empty space
    final double offsetX = (size.width - imageSize.width * scale) / 2;
    final double offsetY = (size.height - imageSize.height * scale) / 2;

    // Define the red paint with stroke width 2
    final Paint paint = Paint()
      ..color = Colors.red // Red color
      ..style = PaintingStyle.stroke // Only stroke (no fill)
      ..strokeWidth = 2.0; // 2 pixels width

    // Get bounding box of the first detected face
    final Rect boundingBox = face.boundingBox;

    // Scale and position the bounding box correctly on the canvas
    final Rect scaledBox = Rect.fromLTRB(
      boundingBox.left * scale + offsetX,
      boundingBox.top * scale + offsetY,
      boundingBox.right * scale + offsetX,
      boundingBox.bottom * scale + offsetY,
    );

    // Draw the face bounding box
    canvas.drawRect(scaledBox, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
