import 'dart:developer';
import 'dart:math' as mth;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';
import 'FacePainter.dart';
import 'package:camera/camera.dart';
import 'package:tflite_flutter/tflite_flutter.dart';
import 'package:audioplayers/audioplayers.dart';

class MeditateScreen extends StatefulWidget {
  const MeditateScreen({super.key, required this.title});

  final String title;

  @override
  State<MeditateScreen> createState() => _MeditateScreenState();
}

// Class to represent the output of detectFace method
class FaceDetectionResult {
  final InputImage inputImage;
  final List<Face> faces;

  FaceDetectionResult({required this.inputImage, required this.faces});
}

// Class to represent the bounding box
class PreviousBoundingBox {
  final double left;
  final double top;
  final double right;
  final double bottom;

  PreviousBoundingBox({
    required this.left,
    required this.top,
    required this.right,
    required this.bottom,
  });
}

class _MeditateScreenState extends State<MeditateScreen> {
  // variables declaration
  late CameraController _cameraController;
  late List<CameraDescription> cameras;
  late FaceDetector _faceDetector;
  late Interpreter _interpreter;
  bool _isCameraInitialized = false;
  List<Face>? _faces;
  String _output = "No Prediction";
  bool _isAudioPlaying = false;
  final player = AudioPlayer();
  final int movementThreshold = 10;
  PreviousBoundingBox? previousBoundingBox;
  String _movingState = "Detecting..";
  String _eyeState = "Detecting..";

  @override
  void initState() {
    super.initState();
    _loadModel();
    log('Model loaded Successfully', name: 'MODEL');
    _initCamera();
  }

  // Camera setting up...
  Future<void> _initCamera() async {
    cameras = await availableCameras();
    _cameraController = CameraController(
      cameras[1],
      ResolutionPreset.high,
      enableAudio: false,
      imageFormatGroup: ImageFormatGroup.yuv420,
    );

    try {
      await _cameraController.initialize();
      setState(() {
        _isCameraInitialized = true;
      });
    } catch (e) {
      print('Error initializing camera: ${e}');
    }
    _cameraController.startImageStream((CameraImage image) {
      _detectAndProcessFaces(image);
    });
    log('Camera Resolution: ${_cameraController.value.previewSize?.width} x ${_cameraController.value.previewSize?.height}',
        name: 'RESOLUTION');
    log('Camera Format: ${_cameraController.value.description}',
        name: 'CAMERA_DESCRIPTION');

    log(_detectAndProcessFaces.toString(), name: 'panther');
  }

  void _loadModel() async {
    try {
      _interpreter = await Interpreter.fromAsset('assets/model.tflite');
    } catch (e) {
      log('Error loading the interpreter', name: 'INTERPRETER_CHECK');
    }

    _faceDetector = FaceDetector(
        options: FaceDetectorOptions(
            enableClassification: true,
            enableContours: true,
            enableLandmarks: true));
  }

  Future<void> _detectAndProcessFaces(CameraImage cameraImage) async {
    final result = await detectFaces(cameraImage);
    if (result != null && result.faces.isNotEmpty) {
      log(result.faces.toString(), name: 'ALL_FACES');
      setState(() {
        // Update the UI to mark the faces using the _faces variable
        _faces = result.faces;
      });
      final firstFace = result.faces.first;
      try {
        _processFace(result.inputImage, firstFace);
      } catch (e) {
        log(e.toString(), name: 'PROCESS_FACE');
      }
    }
  }

  Future<FaceDetectionResult?> detectFaces(CameraImage cameraImage) async {
    log(cameraImage.toString(), name: 'horse');

    // Convert CameraImage to InputImage for MLKit
    final inputImage = _inputImageFromCameraImage(cameraImage);

    if (inputImage == null) {
      log('Failed to convert CameraImage to InputImage', name: 'yaar');
      return null;
    }

    log(inputImage.toString(), name: 'ASDFG');

    // Process the image for face detection
    try {
      final faces = await _faceDetector.processImage(inputImage);
      log('Face Detected: ${faces.toString()}', name: 'DETECTED_FACES');
      return FaceDetectionResult(inputImage: inputImage, faces: faces);
    } catch (e) {
      log('Error Encountered in Detecting Faces: ${e.toString()}',
          name: 'FACE_ERROR');
      return null;
    }
  }

  final Map<DeviceOrientation, int> _orientations = {
    DeviceOrientation.portraitUp: 0,
    DeviceOrientation.landscapeLeft: 90,
    DeviceOrientation.portraitDown: 180,
    DeviceOrientation.landscapeRight: 270,
  };

  InputImage? _inputImageFromCameraImage(CameraImage image) {
    if (cameras.isEmpty) {
      log('Camera not initialized', name: 'CAMERA_ERROR');
      return null;
    }

    final camera = cameras[1];
    final sensorOrientation = camera.sensorOrientation;

    int? rotationCompensation =
        _orientations[_cameraController.value.deviceOrientation];
    if (rotationCompensation == null) return null;

    if (camera.lensDirection == CameraLensDirection.front) {
      rotationCompensation = (sensorOrientation + rotationCompensation) % 360;
    } else {
      rotationCompensation =
          (sensorOrientation - rotationCompensation + 360) % 360;
    }

    final rotation = InputImageRotationValue.fromRawValue(rotationCompensation);
    if (rotation == null) {
      log('Invalid rotation value', name: 'ROTATION_ERROR');
      return null;
    }

    // Convert YUV_420_888 to NV21
    final nv21Bytes = _convertYUV420ToNV21(image);
    if (nv21Bytes == null) {
      log('Failed to convert YUV_420_888 to NV21',
          name: 'FORMAT_CONVERSION_ERROR');
      return null;
    }

    // Create InputImage with the converted NV21 bytes
    return InputImage.fromBytes(
      bytes: nv21Bytes,
      metadata: InputImageMetadata(
        size: Size(image.width.toDouble(), image.height.toDouble()),
        rotation: rotation,
        format: InputImageFormat.nv21,
        bytesPerRow: image.planes[0].bytesPerRow,
      ),
    );
  }

  Uint8List? _convertYUV420ToNV21(CameraImage image) {
    final int width = image.width;
    final int height = image.height;

    // Get Y, U, and V planes
    final Uint8List yPlane = image.planes[0].bytes;
    final Uint8List uPlane = image.planes[1].bytes;
    final Uint8List vPlane = image.planes[2].bytes;

    // Create a Uint8List with NV21 format
    final nv21Bytes = Uint8List(width * height + (width * height ~/ 2));

    // Copy Y plane
    int yIndex = 0;
    for (int i = 0; i < height; i++) {
      int rowOffset = i * image.planes[0].bytesPerRow;
      nv21Bytes.setRange(
          yIndex, yIndex + width, yPlane.sublist(rowOffset, rowOffset + width));
      yIndex += width;
    }

    // Copy U and V planes in NV21 format (VU interleave)
    int uvIndex = width * height;
    for (int i = 0; i < height ~/ 2; i++) {
      int uRowOffset = i * image.planes[1].bytesPerRow;
      int vRowOffset = i * image.planes[2].bytesPerRow;
      for (int j = 0; j < width ~/ 2; j++) {
        nv21Bytes[uvIndex++] = vPlane[vRowOffset + j];
        nv21Bytes[uvIndex++] = uPlane[uRowOffset + j];
      }
    }

    return nv21Bytes;
  }

  void _processFace(InputImage inputImage, Face firstFace) {
    try {
      final boundingBox = firstFace.boundingBox;
      final currentBoundingBox = PreviousBoundingBox(
          left: boundingBox.left,
          top: boundingBox.top,
          right: boundingBox.right,
          bottom: boundingBox.bottom);

      try {
        double? leftEyeOpen = firstFace.leftEyeOpenProbability;
        double? rightEyeOpen = firstFace.rightEyeOpenProbability;

        log(leftEyeOpen.toString() + "--" + rightEyeOpen.toString(),
            name: "EYE_STATE");

        if (leftEyeOpen != null && leftEyeOpen < 0.6 ||
            rightEyeOpen != null && rightEyeOpen < 0.6) {
          setState(() {
            _eyeState = "Closed";
          });
        } else if (leftEyeOpen! > 0.6 || rightEyeOpen! > 0.6) {
          setState(() {
            _eyeState = "Open";
            _playEyeAudio();
          });
        } else {
          setState(() {
            _eyeState = "Detecting..";
          });
        }
      } catch (e) {
        log(e.toString(), name: "EYE_ERROR");
      }

      checkMovement(currentBoundingBox);

      setState(() {
        _output = "State $_movingState, Eye State $_eyeState";
      });
    } catch (e) {
      log(e.toString(), name: 'CHECK_PROCESS');
    }
  }

  // Function to calculate movement and check if it exceeds the threshold
  void checkMovement(PreviousBoundingBox currentBoundingBox) {
    if (previousBoundingBox != null) {
      // Calculate the distance between the previous and current bounding box centers
      log(
          currentBoundingBox.left.toString() +
              "--" +
              currentBoundingBox.top.toString() +
              "--" +
              currentBoundingBox.right.toString() +
              "--" +
              currentBoundingBox.bottom.toString() +
              "-|-" +
              previousBoundingBox!.left.toString() +
              "--" +
              previousBoundingBox!.top.toString() +
              "--" +
              previousBoundingBox!.right.toString() +
              "--" +
              previousBoundingBox!.bottom.toString() +
              "-|-",
          name: "BOUNDING_VALUES");

      try {
        final double currentCenterX =
            (currentBoundingBox.left + currentBoundingBox.right) / 2;

        final double currentCenterY =
            (currentBoundingBox.top + currentBoundingBox.bottom) / 2;

        final double previousCenterX =
            (previousBoundingBox!.left + previousBoundingBox!.right) / 2;
        final double previousCenterY =
            (previousBoundingBox!.top + previousBoundingBox!.bottom) / 2;

        log(
            currentCenterX.toString() +
                "--" +
                currentCenterY.toString() +
                "--" +
                previousCenterX.toString() +
                "--" +
                previousCenterY.toString(),
            name: "DISTANCE_CHECK");

        final double distance = mth.sqrt(
            mth.pow(currentCenterX - previousCenterX, 2) +
                mth.pow(currentCenterY - previousCenterY, 2));

        log(distance.toString(), name: "DISTANCE");

        // Check if the movement exceeds the threshold
        if (distance > movementThreshold) {
          setState(() {
            _movingState = "Moving";
          });
          _playMovement();
        } else {
          setState(() {
            _movingState = "Not Moving";
          });
        }
      } catch (e) {
        log(e.toString(), name: "DISTANCE_CALCULATION_ERROR");
      }
    }

    // Update the previous bounding box
    setState(() {
      previousBoundingBox = currentBoundingBox;
    });
  }

  void _playMovement() async {
    if (!_isAudioPlaying) {
      setState(() {
        _isAudioPlaying = true;
      });

      await player.play(AssetSource('audio/moving.mp3'));

      player.onPlayerComplete.listen((event) {
        setState(() {
          _isAudioPlaying = false;
        });
      });
    }
  }

  void _playEyeAudio() async {
    if (!_isAudioPlaying) {
      setState(() {
        _isAudioPlaying = true;
      });

      await player.play(AssetSource('audio/eye.mp3'));

      player.onPlayerComplete.listen((event) {
        setState(() {
          _isAudioPlaying = false;
        });
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('${widget.title}\n$_output'),
      ),
      body: _isCameraInitialized
          ? SingleChildScrollView(
              child: Column(
                // Make the screen scrollable
                children: [
                  SizedBox(
                    height: 16,
                  ),
                  Center(
                    child: LayoutBuilder(
                      builder: (context, constraints) {
                        return Column(
                          children: [
                            Stack(
                              children: [
                                CameraPreview(_cameraController),
                                if (_faces != null)
                                  CustomPaint(
                                    size: Size(
                                      _cameraController
                                              .value.previewSize?.width ??
                                          0,
                                      _cameraController
                                              .value.previewSize?.height ??
                                          0,
                                    ),
                                    painter: FacePainter(
                                      faces: _faces!,
                                      imageSize: Size(
                                        _cameraController
                                                .value.previewSize?.width ??
                                            0,
                                        _cameraController
                                                .value.previewSize?.height ??
                                            0,
                                      ),
                                    ),
                                  ),
                              ],
                            ),
                            // Additional content below the camera preview if needed
                            Padding(
                              padding: const EdgeInsets.all(16.0),
                              child: Text(
                                'Scroll to see more content',
                                style: TextStyle(fontSize: 18),
                              ),
                            ),
                          ],
                        );
                      },
                    ),
                  ),
                ],
              ),
            )
          : Center(child: CircularProgressIndicator()),
    );
  }

  @override
  void dispose() {
    _cameraController.dispose();
    _faceDetector.close();
    _interpreter.close();
    _faceDetector.close();
    super.dispose();
  }
}
