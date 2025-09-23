// Implementation of BluetoothLogger
#include "logger.h"
#include <stdarg.h>

// Conservative max message size to format before framing/encoding
static const size_t MAX_MSG = 192;

BluetoothLogger::BluetoothLogger(Stream &out)
    : _out(out), _mirror(nullptr), _minLevel(BTLOG_INFO)
{
  _tag[0] = '\0';
}

void BluetoothLogger::setLevel(BtLogLevel level) { _minLevel = level; }
BtLogLevel BluetoothLogger::level() const { return _minLevel; }

void BluetoothLogger::setTag(const char *tag)
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

const char *BluetoothLogger::tag() const { return _tag; }

void BluetoothLogger::setMirror(Stream *mirror) { _mirror = mirror; }

void BluetoothLogger::trace(const char *fmt, ...)
{
  va_list ap;
  va_start(ap, fmt);
  vlogf(BTLOG_TRACE, fmt, ap);
  va_end(ap);
}
void BluetoothLogger::debug(const char *fmt, ...)
{
  va_list ap;
  va_start(ap, fmt);
  vlogf(BTLOG_DEBUG, fmt, ap);
  va_end(ap);
}
void BluetoothLogger::info(const char *fmt, ...)
{
  va_list ap;
  va_start(ap, fmt);
  vlogf(BTLOG_INFO, fmt, ap);
  va_end(ap);
}
void BluetoothLogger::warn(const char *fmt, ...)
{
  va_list ap;
  va_start(ap, fmt);
  vlogf(BTLOG_WARN, fmt, ap);
  va_end(ap);
}
void BluetoothLogger::error(const char *fmt, ...)
{
  va_list ap;
  va_start(ap, fmt);
  vlogf(BTLOG_ERROR, fmt, ap);
  va_end(ap);
}

void BluetoothLogger::logf(BtLogLevel level, const char *fmt, ...)
{
  va_list ap;
  va_start(ap, fmt);
  vlogf(level, fmt, ap);
  va_end(ap);
}

void BluetoothLogger::vlogf(BtLogLevel level, const char *fmt, va_list args)
{
  if (level < _minLevel)
    return;

  char buf[MAX_MSG];
  vsnprintf(buf, sizeof(buf), fmt, args);
  buf[sizeof(buf) - 1] = '\0';
  writeFramed(level, buf);
}

void BluetoothLogger::writeFramed(BtLogLevel level, const char *msg)
{
  // Line protocol: L|level|millis|tag|message\n
  _out.print('L');
  _out.print('|');
  _out.print((int)level);
  _out.print('|');
  _out.print(millis());
  _out.print('|');
  percentEncode(_tag, _out);
  _out.print('|');
  percentEncode(msg, _out);
  _out.print('\n');

  if (_mirror)
  {
    _mirror->print('L');
    _mirror->print('|');
    _mirror->print((int)level);
    _mirror->print('|');
    _mirror->print(millis());
    _mirror->print('|');
    percentEncode(_tag, *_mirror);
    _mirror->print('|');
    percentEncode(msg, *_mirror);
    _mirror->print('\n');
  }
}

void BluetoothLogger::flush()
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

const char *BluetoothLogger::levelToStr(BtLogLevel level)
{
  switch (level)
  {
  case BTLOG_TRACE:
    return "TRACE";
  case BTLOG_DEBUG:
    return "DEBUG";
  case BTLOG_INFO:
    return "INFO";
  case BTLOG_WARN:
    return "WARN";
  case BTLOG_ERROR:
    return "ERROR";
  default:
    return "?";
  }
}

// Percent-encode '|' and '\n' and any non-printable bytes to keep the frame one line
void BluetoothLogger::percentEncode(const char *in, Stream &s)
{
  if (!in)
    return;
  for (const unsigned char *p = (const unsigned char *)in; *p; ++p)
  {
    unsigned char c = *p;
    bool safe = (c >= 0x20 && c <= 0x7E && c != '|' && c != '%');
    if (safe)
    {
      s.write(c);
    }
    else
    {
      const char hex[] = "0123456789ABCDEF";
      s.write('%');
      s.write(hex[(c >> 4) & 0xF]);
      s.write(hex[c & 0xF]);
    }
  }
}
