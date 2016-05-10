#!/bin/bash

memcached -u memcache -l 0.0.0.0 $@
