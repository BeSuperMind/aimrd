import 'dart:developer';
import 'dart:typed_data';
import 'dart:math' as mth;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';
import 'FacePainter.dart';
import 'package:camera/camera.dart';
import 'package:tflite_flutter/tflite_flutter.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:image/image.dart' as img;

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
  late CameraController _cameraController;
  late List<CameraDescription> cameras;
  late FaceDetector _faceDetector;
  late Interpreter _interpreter;
  bool _isCameraInitialized = false;
  List<Face>? _faces;
  String _output = "No Prediction";
  bool _isAudioPlaying = false;
  final player = AudioPlayer();
  final int movementThreshold = 15;
  PreviousBoundingBox? previousBoundingBox;

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

    _faceDetector = FaceDetector(options: FaceDetectorOptions());
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
        _processFaceForModel(result.inputImage, firstFace);
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

  // Function to calculate movement and check if it exceeds the threshold
  void checkMovement(PreviousBoundingBox currentBoundingBox) {
    if (previousBoundingBox != null) {
      // Calculate the distance between the previous and current bounding box centers
      final double prevCenterX =
          (previousBoundingBox!.left + previousBoundingBox!.right) / 2;
      final double prevCenterY =
          (previousBoundingBox!.top + previousBoundingBox!.bottom) / 2;

      final double currCenterX =
          (currentBoundingBox.left + currentBoundingBox.right) / 2;
      final double currCenterY =
          (currentBoundingBox.top + currentBoundingBox.bottom) / 2;

      final double distance = mth.sqrt(mth.pow(currCenterX - prevCenterX, 2) +
          mth.pow(currCenterY - prevCenterY, 2));

      // Check if the movement exceeds the threshold
      if (distance > movementThreshold) {
        _playMovement();
      }
    }

    // Update the previous bounding box
    previousBoundingBox = currentBoundingBox;
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

  void _processFaceForModel(InputImage inputImage, Face firstFace) {
    try {
      final boundingBox = firstFace.boundingBox;
      final imageWidth = inputImage.metadata!.size.width.toInt();
      final imageHeight = inputImage.metadata!.size.height.toInt();
      final xImage = boundingBox.left.toInt().clamp(0, imageWidth - 1);
      final yImage = boundingBox.top.toInt().clamp(0, imageHeight - 1);
      final widthImage =
          boundingBox.width.toInt().clamp(0, imageWidth - xImage);
      final heightImage =
          boundingBox.height.toInt().clamp(0, imageHeight - yImage);
      log('Starting the function, executed here ', name: 'CHECK_EXECUTION');

      // Crop the face from the image
      final faceImage = img.copyCrop(
          img.Image.fromBytes(
            width: widthImage,
            height: heightImage,
            bytes: inputImage.bytes!.buffer,
          ),
          x: xImage,
          y: yImage,
          width: widthImage,
          height: heightImage);

      log('running the Process Face For Model function', name: 'BUILD');
      // Resize the cropped face to 48x48 and 24x24
      final resized48x48 = img.copyResize(faceImage, width: 48, height: 48);
      final resized24x24 = img.copyResize(faceImage, width: 24, height: 24);

      // Convert the resized images to grayscale
      final grayscale48x48 = img.grayscale(resized48x48);
      final grayscale24x24 = img.grayscale(resized24x24);

      // Convert the grayscale images to float32 tensors
      final input1 = imageToTensor(grayscale48x48); // Face image tensor
      final input2 = imageToTensor(grayscale24x24); // Eye image tensor

      // Outputs for the model
      // final emotionOutput =
      //     List<double>.filled(7, 0.0); // 7 classes for emotions
      final emotionOutput =
          List<List<double>>.generate(1, (_) => List<double>.filled(7, 0.0));
      // final eyeOutput =
      //     List<double>.filled(1, 0.0); // Single value for eye state
      final eyeOutput =
          List<List<double>>.generate(1, (_) => List<double>.filled(1, 0.0));
      final outputs = {
        0: eyeOutput,
        1: emotionOutput,
      };

      try {
        // Run the TensorFlow Lite model
        _interpreter.runForMultipleInputs([input1, input2], outputs);
      } catch (e) {
        log(e.toString(), name: 'MODEL_ERROR');
      }
      log(outputs.toString(), name: 'MODEL_OUTPUT');

      // Process the emotion output
      final flattenedEmotionOutput = emotionOutput[0]; // Extract the inner list
      final emotionLabelIndex = flattenedEmotionOutput.indexWhere((value) =>
          value == flattenedEmotionOutput.reduce((a, b) => a > b ? a : b));
      final labelsDict = {
        0: 'Angry',
        1: 'Disgust',
        2: 'Fear',
        3: 'Happy',
        4: 'Neutral',
        5: 'Sad',
        6: 'Surprise',
      };
      final emotionText = labelsDict[emotionLabelIndex] ?? 'Unknown';

      // Process the eye state output
      final eyeState =
          eyeOutput[0][0] < 0.5 ? 'Close' : 'Open'; // Access the inner value

      // Log or display the results
      print('Emotion: $emotionText');
      print('Eye State: $eyeState');

      setState(() {
        _output = 'Emotion: $emotionText Eye State: $eyeState';
      });

      if (eyeState == 'Open') {
        _playEyeAudio();
      }
    } catch (e) {
      log(e.toString(), name: 'CHECK_PROCESS');
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

  List<List<List<List<double>>>> addBatchAndChannelDimensions(img.Image image) {
    final height = image.height;
    final width = image.width;

    // Create a 4D List with batch size 1 and channel size 1
    final output = List.generate(
      1, // Batch size
      (_) => List.generate(
        height,
        (y) => List.generate(
          width,
          (x) {
            final pixel = image.getPixel(x, y);

            // Set the pixel's normalized position in the range [0, 1]
            pixel.setPositionNormalized(x / width, y / height);

            // Convert normalized grayscale value
            final normalizedValue =
                pixel.luminanceNormalized as double; // Get normalized grayscale

            return [normalizedValue]; // Wrap in channel
          },
        ),
      ),
    );

    return output;
  }

  List<List<List<List<double>>>> imageToTensor(img.Image image) {
    return addBatchAndChannelDimensions(image);
  }

  Uint8List convertToModelInput(
      Uint8List grayscaleData, int width, int height) {
    // Decode Uint8List to an image, resize it to 48x48
    final image = img.Image.fromBytes(
      width: width,
      height: height,
      bytes: grayscaleData.buffer,
      format: img.Format.float32,
    );

    final resizedImage = img.copyResize(image, width: 48, height: 48);

    // Flatten the 48x48 grayscale image to a 1D list of length 48*48
    final grayscaleFlattened = resizedImage.getBytes();

    // Convert to Float32 for model input
    final input = Float32List.fromList(
      grayscaleFlattened
          .map((pixel) => pixel / 255.0)
          .toList(), // Normalize pixels
    );

    return input.buffer.asUint8List();
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
