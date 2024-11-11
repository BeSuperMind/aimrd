import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'meditate_try.dart';

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

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
            title: const Text('Quantum Coherence Technologies'),
            backgroundColor: Colors.deepPurple),
        body: _currentIndexValue == 0
            ? const Center(
                child: Text(
                  'Welcome, Try our meditating feature powered with Deep Learning models. Click on Meditate button to start meditating',
                  style: TextStyle(fontSize: 20.0),
                  textAlign: TextAlign.center,
                ),
              )
            : const MeditateScreen(), // Display MeditateScreen when Meditate tab is selected
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
