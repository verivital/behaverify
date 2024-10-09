#!/bin/bash

./compare_timing.sh
sleep 10
./pipeline_existing_design_time.sh
shutdown now
