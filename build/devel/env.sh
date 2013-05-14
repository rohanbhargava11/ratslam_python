#!/usr/bin/env sh
# generated from catkin/cmake/templates/env.sh.in

if [ $# -eq 0 ] ; then
  /bin/echo "Entering environment at '/home/rohan/thesis_work_code/ratslam_python/build/devel', type 'exit' to leave"
  . "/home/rohan/thesis_work_code/ratslam_python/build/devel/setup.sh"
  "$SHELL" -i
  /bin/echo "Exiting environment at '/home/rohan/thesis_work_code/ratslam_python/build/devel'"
else
  . "/home/rohan/thesis_work_code/ratslam_python/build/devel/setup.sh"
  exec "$@"
fi
