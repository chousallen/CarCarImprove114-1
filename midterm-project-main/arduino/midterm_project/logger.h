// Simple Bluetooth logger for Arduino
// Sends structured log lines over a Stream (e.g., Serial3 to HC-06)

#pragma once

#include <Arduino.h>

enum LogLevel : uint8_t
{
  LOG_VERBOSE = 0,
  LOG_DEBUG = 1,
  LOG_INFO = 2,
  LOG_WARN = 3,
  LOG_ERROR = 4,
};

class logger
{
public:
  // Copy constructor
  logger(const logger &other, const char *tag = nullptr);
  // Construct a logger and assign a tag immediately
  logger(Stream &out, const char *tag);

  // Minimum level to emit. Messages below this level are dropped.
  void setLevel(LogLevel level);
  LogLevel level() const;

  // Optional human-readable tag (e.g., module/component). Max 20 chars stored.
  void setTag(const char *tag);
  const char *tag() const;

  // Mirror logs to an additional Stream for local debugging (e.g., Serial)
  void setMirror(Stream *mirror);

  // Printf-style logging APIs
  void verbose(const char *fmt, ...);
  void debug(const char *fmt, ...);
  void info(const char *fmt, ...);
  void warn(const char *fmt, ...);
  void error(const char *fmt, ...);

  // Core log function (printf-style). Usually not needed directly.
  void logf(LogLevel level, const char *fmt, ...);

  // Flush output streams if supported
  void flush();

private:
  Stream &_out;
  Stream *_mirror; // optional
  LogLevel _minLevel;
  char _tag[21];

  void vlogf(LogLevel level, const char *fmt, va_list args);
  void writeFramed(LogLevel level, const char *msg);

  static const char *levelToStr(LogLevel level);
  static void percentEncode(const char *in, Stream &s);
};