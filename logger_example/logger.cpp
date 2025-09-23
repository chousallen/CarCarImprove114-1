// Implementation of logger
// This file implements a simple logger for Arduino that outputs structured log lines
// in the format: <level>|<timestamp>|<tag>|<message>\n, with percent-encoding for special characters.
#include "logger.h"
#include <stdarg.h>
#include <string.h>

// Conservative max message size to format before framing/encoding
// This buffer size limits the maximum length of a single log message.
static const size_t MAX_MSG = 192;

// Constructor with tag: forwards to base constructor setup and sets tag
logger::logger(Stream &out, const char *tag)
    : _out(out), _mirror(nullptr), _minLevel(LOG_INFO)
{
  _tag[0] = '\0';
  setTag(tag);
}

// Copy constructor: copies logger configuration and streams.
// If tag is provided (non-null), overrides the copied tag; otherwise preserves other's tag.
logger::logger(const logger &other, const char *tag)
    : _out(other._out), _mirror(other._mirror), _minLevel(other._minLevel)
{
  if (tag)
  {
    setTag(tag);
  }
  else
  {
    strncpy(_tag, other._tag, sizeof(_tag));
    _tag[sizeof(_tag) - 1] = '\0';
  }
}

// Set the minimum log level to emit
void logger::setLevel(LogLevel level) { _minLevel = level; }
// Get the current minimum log level
LogLevel logger::level() const { return _minLevel; }

// Set a human-readable tag for log messages (e.g., module/component)
void logger::setTag(const char *tag)
{
  if (!tag)
  {
    _tag[0] = '\0';
    return;
  }
  // copy up to 20 chars
  size_t i = 0;
  for (; i < sizeof(_tag) - 1 && tag[i]; ++i)
  {
    _tag[i] = tag[i];
  }
  _tag[i] = '\0';
}

// Get the current tag
const char *logger::tag() const { return _tag; }

// Set an optional mirror stream for local debugging (e.g., Serial)
void logger::setMirror(Stream *mirror) { _mirror = mirror; }

// Log a verbose-level message (lowest priority)
void logger::verbose(const char *fmt, ...)
{
  va_list ap;
  va_start(ap, fmt);
  vlogf(LOG_VERBOSE, fmt, ap);
  va_end(ap);
}
// Log a debug-level message
void logger::debug(const char *fmt, ...)
{
  va_list ap;
  va_start(ap, fmt);
  vlogf(LOG_DEBUG, fmt, ap);
  va_end(ap);
}
// Log an info-level message
void logger::info(const char *fmt, ...)
{
  va_list ap;
  va_start(ap, fmt);
  vlogf(LOG_INFO, fmt, ap);
  va_end(ap);
}
// Log a warning-level message
void logger::warn(const char *fmt, ...)
{
  va_list ap;
  va_start(ap, fmt);
  vlogf(LOG_WARN, fmt, ap);
  va_end(ap);
}
// Log an error-level message (highest priority)
void logger::error(const char *fmt, ...)
{
  va_list ap;
  va_start(ap, fmt);
  vlogf(LOG_ERROR, fmt, ap);
  va_end(ap);
}

// Core log function with explicit log level (printf-style)
void logger::logf(LogLevel level, const char *fmt, ...)
{
  va_list ap;
  va_start(ap, fmt);
  vlogf(level, fmt, ap);
  va_end(ap);
}

// Internal: log with va_list for variadic functions
void logger::vlogf(LogLevel level, const char *fmt, va_list args)
{
  if (level < _minLevel)
    return;

  char buf[MAX_MSG];
  vsnprintf(buf, sizeof(buf), fmt, args);
  buf[sizeof(buf) - 1] = '\0';
  writeFramed(level, buf);
}

// Internal: format and write a structured log line to the output stream(s)
// Format: <level letter>|<timestamp>|<tag>|<message>\n
// level: V=VERBOSE, D=DEBUG, I=INFO, W=WARN, E=ERROR
// timestamp: millis() value
// tag: percent-encoded tag string
// message: percent-encoded log message
void logger::writeFramed(LogLevel level, const char *msg)
{
  // Line protocol: level(a letter)|timestamp|tag|message\n
  char levelChar;
  switch (level)
  {
  case LOG_VERBOSE:
    levelChar = 'V';
    break;
  case LOG_DEBUG:
    levelChar = 'D';
    break;
  case LOG_INFO:
    levelChar = 'I';
    break;
  case LOG_WARN:
    levelChar = 'W';
    break;
  case LOG_ERROR:
    levelChar = 'E';
    break;
  default:
    levelChar = '?';
    break;
  }

  _out.print(levelChar);
  _out.print(':');
  _out.print(millis());
  _out.print(":{");
  percentEncode(_tag, _out);
  _out.print("}:");
  percentEncode(msg, _out);
  _out.print('\n');

  if (_mirror)
  {
    _mirror->print(levelChar);
    _mirror->print(':');
    _mirror->print(millis());
    _mirror->print(":{");
    percentEncode(_tag, *_mirror);
    _mirror->print("}:");
    percentEncode(msg, *_mirror);
    _mirror->print('\n');
  }
}

// Flush output streams if supported (no-op for most Arduino Streams)
void logger::flush()
{
  if (_out.availableForWrite())
  {
    // Some Streams don't implement flush meaningfully; this is a no-op.
  }
  if (_mirror && _mirror->availableForWrite())
  {
    // no-op
  }
}

// Convert log level enum to string for display
const char *logger::levelToStr(LogLevel level)
{
  switch (level)
  {
  case LOG_VERBOSE:
    return "VERBOSE";
  case LOG_DEBUG:
    return "DEBUG";
  case LOG_INFO:
    return "INFO";
  case LOG_WARN:
    return "WARN";
  case LOG_ERROR:
    return "ERROR";
  default:
    return "?";
  }
}

// Percent-encode '|' and '\n' and any non-printable bytes to keep the frame one line
// Percent-encode '|', '\n', '%' and non-printable bytes to keep the log frame on one line
void logger::percentEncode(const char *in, Stream &s)
{
  if (!in)
    return;
  for (const unsigned char *p = (const unsigned char *)in; *p; ++p)
  {
    unsigned char c = *p;
    bool safe = (c >= 0x20 && c <= 0x7E);
    if (safe)
    {
      s.write(c);
    }
    // else
    // {
    //   const char hex[] = "0123456789ABCDEF";
    //   s.write('%');
    //   s.write(hex[(c >> 4) & 0xF]);
    //   s.write(hex[c & 0xF]);
    // }
  }
}
