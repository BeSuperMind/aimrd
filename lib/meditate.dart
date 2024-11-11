import 'dart:async';
import 'package:audioplayers/audioplayers.dart';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:image/image.dart' as img;
import 'package:tflite_flutter/tflite_flutter.dart';
import 'dart:math' as math;
import 'main.dart';
import 'dart:typed_data';

class MeditateScreen extends StatefulWidget {
  const MeditateScreen({super.key});

  @override
  State<MeditateScreen> createState() => _MeditateScreenState();
}

class _MeditateScreenState extends State<MeditateScreen> {
  CameraImage? cameraImage;
  CameraController? cameraController;
  Interpreter? interpreter;
  List<String>? labels;
  String _output = 'Loading...';
  final AudioPlayer _audioPlayer = AudioPlayer();

  @override
  void initState() {
    super.initState();
    loadCamera();
    loadModelAndLabels();
  }

  Future<void> loadCamera() async {
    cameras = await availableCameras();
    cameraController = CameraController(cameras![1], ResolutionPreset.medium);
    await cameraController!.initialize();

    if (!mounted) return;
    setState(() {
      cameraController!.startImageStream((imageStream) {
        cameraImage = imageStream;

        runModel();
      });
    });
  }

  Future<void> loadModelAndLabels() async {
    try {
      interpreter = await Interpreter.fromAsset('assets/model.tflite');
      labels = await loadLabels(
          'assets/labels.txt'); // Adjust if labels are separate
    } catch (e) {
      print("Error loading model or labels: $e");
    }
  }

  Future<List<String>> loadLabels(String path) async {
    final content = await DefaultAssetBundle.of(context).loadString(path);
    return content.split('\n');
  }

  Future<void> runModel() async {
    if (cameraImage != null && interpreter != null) {
      // Preprocess the image using the image package
      final resizedImage = img.copyResize(
        img.grayscale(img.Image.fromBytes(
          width: cameraImage!.width,
          height: cameraImage!.height,
          bytes: cameraImage!.planes[0].bytes.buffer, // Use buffer property
        )),
        width: 48,
        height: 48,
      );

      // Convert the image to a list of pixel values
      final inputData =
          resizedImage.getBytes().map((pixel) => pixel / 255.0).toList();

      // Reshape the input data into the expected tensor shape
      final inputTensor = Float32List.fromList(inputData);

      // Assuming your model has separate inputs for face and eye:
      var faceInput = inputTensor.sublist(0, 48 * 48);
      var eyeInput = inputTensor.sublist(48 * 48);

      // ... rest of your model inference code ...
      var outputBuffer =
          List.filled(7, 0.0); // Adjust based on model output size
      interpreter!.run([faceInput, eyeInput], outputBuffer);

      var maxIndex = outputBuffer.indexOf(outputBuffer.reduce(math.max));

      setState(() {
        _output =
            "${labels![maxIndex]} | Eyes: ${outputBuffer[6] < 0.5 ? 'Closed' : 'Open'}";
      });

      // Play audio based on emotion or eye state (adjust logic as needed)
      if (outputBuffer[6] < 0.5) {
        await _audioPlayer.play('assets/audio/concentrate.mp3'
            as Source); // Replace with your audio filename
      }
    }
  }

  @override
  void dispose() {
    cameraController?.dispose();
    interpreter?.close();
    _audioPlayer.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Live meditation session by QCT'),
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
