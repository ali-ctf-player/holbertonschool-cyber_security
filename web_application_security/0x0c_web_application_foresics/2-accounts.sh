#!/bin/bash
awk '
/Failed password/ {fail[$9]++}
/Accepted password/ {success[$9]++}
END {
  max = 0
  user = ""
  for (u in success) {
    if (fail[u] > max) {
      max = fail[u]
      user = u
    }
  }
  if (user != "") print user
}' auth.log
