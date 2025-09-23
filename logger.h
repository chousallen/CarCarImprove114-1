// Simple Bluetooth logger for Arduino
// Sends structured log lines over a Stream (e.g., Serial3 to HC-06)

#pragma once

#include <Arduino.h>

enum BtLogLevel : uint8_t
{
  BTLOG_TRACE = 0,
  BTLOG_DEBUG = 1,
  BTLOG_INFO = 2,
  BTLOG_WARN = 3,
  BTLOG_ERROR = 4,
};

class BluetoothLogger
{
public:
  // Construct a logger that writes to the provided Stream (e.g., Serial3)
  explicit BluetoothLogger(Stream &out);

  // Minimum level to emit. Messages below this level are dropped.
  void setLevel(BtLogLevel level);
  BtLogLevel level() const;

  // Optional human-readable tag (e.g., module/component). Max 20 chars stored.
  void setTag(const char *tag);
  const char *tag() const;

  // Mirror logs to an additional Stream for local debugging (e.g., Serial)
  void setMirror(Stream *mirror);

  // Printf-style logging APIs
  void trace(const char *fmt, ...);
  void debug(const char *fmt, ...);
  void info(const char *fmt, ...);
  void warn(const char *fmt, ...);
  void error(const char *fmt, ...);

  // Core log function (printf-style). Usually not needed directly.
  void logf(BtLogLevel level, const char *fmt, ...);

  // Flush output streams if supported
  void flush();

private:
  Stream &_out;
  Stream *_mirror; // optional
  BtLogLevel _minLevel;
  char _tag[21];

  void vlogf(BtLogLevel level, const char *fmt, va_list args);
  void writeFramed(BtLogLevel level, const char *msg);

  static const char *levelToStr(BtLogLevel level);
  static void percentEncode(const char *in, Stream &s);
};

class logger
{
}