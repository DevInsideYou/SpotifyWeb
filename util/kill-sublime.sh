#!/bin/bash

kill $(ps aux | awk '/[s]ublime_text/ {print $2}')
