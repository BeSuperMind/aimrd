import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:light/light.dart';
import 'tryTwo.dart';

List<CameraDescription>? cameras;
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  cameras = await availableCameras();
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  int _currentIndexValue = 0;
  late Light _light;
  double _lightValue = 0.0;

  @override
  void initState() {
    super.initState();
    _light = Light();
    _light.lightSensorStream.listen((value) {
      setState(() {
        _lightValue = value.toDouble();
      });
    });
  }

  Color _getBarColor(double lightValue) {
    if (lightValue >= 90) {
      return Colors.green;
    } else if (lightValue >= 50) {
      return Colors.yellow;
    } else {
      return Colors.red;
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
            title: const Text('Quantum Coherence Technologies'),
            backgroundColor: Colors.deepPurple),
        body: _currentIndexValue == 0
            ? Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const Center(
                    child: Text(
                      'Welcome, Try our meditating feature powered with Deep Learning models. Click on Meditate button to start meditating',
                      style: TextStyle(fontSize: 20.0),
                      textAlign: TextAlign.center,
                    ),
                  ),
                  const SizedBox(height: 40),
                  Text(
                    'Surrounding Brightness: ${_lightValue.toStringAsFixed(1)} lux',
                    style: const TextStyle(fontSize: 18),
                  ),
                  const SizedBox(height: 20),
                  LinearProgressIndicator(
                    value: _lightValue / 100,
                    backgroundColor: Colors.grey.shade300,
                    color: _getBarColor(_lightValue),
                    minHeight: 20,
                  ),
                  const SizedBox(height: 20),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: const [
                      Text(
                          '• Make sure the above progress bar is green before starting the meditation',
                          style: TextStyle(fontSize: 16)),
                      SizedBox(height: 10),
                      Text(
                        '• The place where the progress bar is green, position yourself in that place as there light is good',
                        style: TextStyle(fontSize: 16),
                      ),
                      SizedBox(height: 10),
                      Text(
                        '• Please make sure that your face is in the direction where your device front side was when the progress bar was green',
                        style: TextStyle(fontSize: 16),
                      ),
                    ],
                  ),
                ],
              )
            : const MeditateScreen(
                title: 'Quantum Coherence',
              ), // Display MeditateScreen when Meditate tab is selected
        bottomNavigationBar: BottomNavigationBar(
          items: const [
            BottomNavigationBarItem(
              label: 'Home',
              icon: Icon(Icons.home),
            ),
            BottomNavigationBarItem(
                label: 'Meditate',
                icon: Icon(
                  Icons.favorite,
                ))
          ],
          currentIndex: _currentIndexValue,
          onTap: (value) {
            setState(() {
              _currentIndexValue =
                  value; // Update current index to switch screens
            });
          },
        ),
      ),
    );
  }
}
