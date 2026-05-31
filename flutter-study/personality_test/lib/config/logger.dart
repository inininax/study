import 'package:logger/logger.dart';

final LoggerService logger = AppLoggerService();

abstract class LoggerService {
  void log(String message);

  void debug(String message);

  void info(String message);

  void warning(String message);

  void error(String message, [dynamic error, StackTrace? stackTrace]);
}

class AppLoggerService implements LoggerService {
  final Logger _logger;

  AppLoggerService()
      : _logger = Logger(
          printer: PrettyPrinter(
            methodCount: 3,
            errorMethodCount: 8,
            lineLength: 120,
            colors: true,
            printEmojis: true,
            printTime: true,
          ),
        );

  @override
  void log(String message) {
    _logger.i(message);
  }

  @override
  void debug(String message) {
    _logger.d(message);
  }

  @override
  void info(String message) {
    _logger.i(message);
  }

  @override
  void warning(String message) {
    _logger.w(message);
  }

  @override
  void error(String message, [dynamic error, StackTrace? stackTrace]) {
    _logger.e(message, error: error, stackTrace: stackTrace);
  }
}
