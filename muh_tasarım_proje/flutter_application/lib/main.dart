import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Kamera cihazları listesi alınıyor
  final cameras = await availableCameras();
  // İlk kamera cihazı seçiliyor
  final firstCamera = cameras.first;
  runApp(MyApp(camera: firstCamera));
}

class MyApp extends StatelessWidget {
  final CameraDescription camera;

  const MyApp({Key? key, required this.camera}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: TakePictureScreen(camera: camera),
    );
  }
}

class TakePictureScreen extends StatefulWidget {
  final CameraDescription camera;

  const TakePictureScreen({Key? key, required this.camera}) : super(key: key);

  @override
  TakePictureScreenState createState() => TakePictureScreenState();
}

class TakePictureScreenState extends State<TakePictureScreen> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;

  @override
  void initState() {
    super.initState();
    // Kamera kontrolcüsü oluşturuluyor
    _controller = CameraController(
      widget.camera,
      ResolutionPreset.medium,
      
    );

    // Kamera kontrolcüsü başlatılıyor
    _initializeControllerFuture = _controller.initialize();
  }

  @override
  void dispose() {
    // Kamera kontrolcüsü kapatılıyor
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color.fromRGBO(31, 31, 31, 25),
      appBar: AppBar(title: Text(''),
      backgroundColor: Color.fromRGBO(24, 24, 24, 20),),
      // Kamera görüntüsünü göstermek için Stack kullanılıyor
      body: Stack(
        children: <Widget>[
        
          Center(
            
            child: Container(
              width: 500.0, // Kare genişliği
              height: 500.0, // Kare yüksekliği
              child: FutureBuilder<void>(
                future: _initializeControllerFuture,
                
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.done) {
                    // Eğer Future tamamlandıysa, kamera görüntüsü gösteriliyor
                    return CameraPreview(_controller);
                  } else {
                    // Eğer Future hala tamamlanmamışsa, bir yüklenme göstergesi gösteriliyor
                    return Center(child: CircularProgressIndicator());
                  }
                },
              ),
            ),
          ),
          // Fotoğraf çekme butonu
          Align(
            alignment: Alignment.bottomCenter,
            child: Padding(
              padding: EdgeInsets.only(bottom: 20.0),
              child: FloatingActionButton(
                child: Icon(Icons.camera),
                onPressed: () async {
                  try {
                    // Kamera görüntüsü alınıyor ve geçici bir dosyaya kaydediliyor
                    final image = await _controller.takePicture();

                    // Görüntü geçici dosyadan kalıcı bir dosyaya kopyalanıyor
                    final appDirectory = await getApplicationDocumentsDirectory();
                    final fileName = DateTime.now().toString();
                    final savedImage = await File(image.path).copy('${appDirectory.path}/$fileName.png');

                    // Görüntü başarıyla kaydedildiğinde bir ileti gösteriliyor
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Picture saved to ${savedImage.path}')),
                    );
                  } catch (e) {
                    // Bir hata oluştuğunda bir ileti gösteriliyor
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Error: $e')),
                    );
                  }
                },
              ),
            ),
          ),
        ],
      ),
    );
  }
}
