import 'dart:ui';

import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:flutter/material.dart';
import 'package:mybudongsan/firebase_options.dart';

import 'config/config.dart';
import 'config/logger.dart';
import 'intro/intro_page.dart';
import 'map/map_sample.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // config
  await Config.load();

  // firebase
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(const MyApp());

  FlutterError.onError = (errorDetails) {
    logger.error("FlutterError.onError", {errorDetails.toString()});
    FirebaseCrashlytics.instance.recordFlutterError(errorDetails);
  };

  PlatformDispatcher.instance.onError = (error, stack) {
    logger.error("PlatformDispatcher.instance.onError", {error, stack});
    FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
    return true;
  };
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '마이 부동산',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const IntroPage(),
      // home: const MapSample(),
    );
  }
}
