import 'dart:async';
import 'package:audioplayers/audioplayers.dart';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:image/image.dart' as img;
import 'package:tflite_flutter/tflite_flutter.dart';
import 'package:google_ml_vision/google_ml_vision.dart';
import 'dart:typed_data';
import 'main.dart';

class MeditateScreen extends StatefulWidget {
  const MeditateScreen({super.key});

  @override
  State<MeditateScreen> createState() => _MeditateScreenState();
}

class _MeditateScreenState extends State<MeditateScreen> {
  CameraController? cameraController;
  Interpreter? interpreter;
  FaceDetector faceDetector = GoogleVision.instance.faceDetector();
  final AudioPlayer _audioPlayer = AudioPlayer();
  List<String>? labels;
  String _output = 'Loading...';
  CameraImage? cameraImage;

  @override
  void initState() {
    super.initState();
    loadCamera();
    loadModelAndLabels();
  }

  Future<void> loadCamera() async {
    cameraController =
        CameraController(cameras![1], ResolutionPreset.ultraHigh);
    await cameraController!.initialize();

    if (!mounted) return;
    setState(() {
      cameraController!.startImageStream((imageStream) {
        cameraImage = imageStream;
        detectFaceAndRunModel();
      });
    });
  }

  Future<void> loadModelAndLabels() async {
    try {
      interpreter = await Interpreter.fromAsset('assets/model.tflite');
      labels = await loadLabels('assets/labels.txt');
    } catch (e) {
      print("Error loading model or labels: $e");
    }
  }

  Future<List<String>> loadLabels(String path) async {
    final content = await DefaultAssetBundle.of(context).loadString(path);
    return content.split('\n');
  }

  Future<void> detectFaceAndRunModel() async {
    if (cameraImage == null || interpreter == null) return;

    final visionImage = GoogleVisionImage.fromBytes(
      cameraImage!.planes[0].bytes,
      buildMetaData(cameraImage!),
    );

    final faces = await faceDetector.processImage(visionImage);

    if (faces.isNotEmpty) {
      // Use the first detected face for this example
      final face = faces[0];
      final faceBoundingBox = face.boundingBox;

      // Convert face region to img.Image and preprocess for model input
      final faceImage = img.copyResize(
        img.Image.fromBytes(
          width: faceBoundingBox.width.toInt(),
          height: faceBoundingBox.height.toInt(),
          bytes: cameraImage!.planes[0].bytes.buffer,
        ),
        width: 48,
        height: 48,
      );

      final inputData =
          faceImage.getBytes().map((pixel) => pixel / 255.0).toList();
      final inputTensor = Float32List.fromList(inputData);
      var faceInput = inputTensor.sublist(0, 48 * 48);
      var eyeInput = inputTensor.sublist(24 * 24);

      var outputBuffer = List.filled(7, 0.0);
      interpreter!.run([faceInput, eyeInput], outputBuffer);

      var maxIndex =
          outputBuffer.indexOf(outputBuffer.reduce((a, b) => a > b ? a : b));

      setState(() {
        _output =
            "${labels![maxIndex]} | Eyes: ${outputBuffer[6] < 0.5 ? 'Closed' : 'Open'}";
      });

      if (outputBuffer[6] >= 0.5) {
        await _audioPlayer.play(AssetSource('audio/moving.mp3'));
      } else if (outputBuffer[6] < 0.5) {
        await _audioPlayer.play(AssetSource('audio/drowsy.mp3'));
      }
    }
  }

  GoogleVisionImageMetadata buildMetaData(CameraImage image) {
    return GoogleVisionImageMetadata(
      size: Size(image.width.toDouble(), image.height.toDouble()),
      rotation: ImageRotation.rotation0,
      planeData: image.planes.map(
        (plane) {
          return GoogleVisionImagePlaneMetadata(
            bytesPerRow: plane.bytesPerRow,
            height: plane.height,
            width: plane.width,
          );
        },
      ).toList(),
    );
  }

  @override
  void dispose() {
    cameraController?.dispose();
    interpreter?.close();
    faceDetector.close();
    _audioPlayer.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Live meditation session by QCT\n${_output}'),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(20),
            child: SizedBox(
              height: MediaQuery.of(context).size.height * 0.7,
              width: MediaQuery.of(context).size.width,
              child: cameraController == null ||
                      !cameraController!.value.isInitialized
                  ? const Center(child: CircularProgressIndicator())
                  : AspectRatio(
                      aspectRatio: cameraController!.value.aspectRatio,
                      child: CameraPreview(cameraController!),
                    ),
            ),
          ),
          Text(
            _output,
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 20),
          ),
        ],
      ),
    );
  }
}
