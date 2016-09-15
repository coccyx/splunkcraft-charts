export CHART_1_QUERY="search eventtype=splunkcraft2016 | timechart span=1d dc(player) AS player"
export CHART_1_ET="-7d@d"
export CHART_1_LT="-0d@d"
export CHART_1_SERIESFIELD="player"
export CHART_1_VALUEFIELD="player"
export CHART_1_COLOR="red"
export CHART_1_TYPE="verticalbar"
export CHART_1_TITLE="Users last 7d"
export CHART_1_XOFFSET=0
export CHART_1_YOFFSET=0
export CHART_1_ZOFFSET=80
export CHART_1_ORIENTATION=0
export CHART_1_MIRROR=0
export CHART_1_TIMER=60
export CHART_2_QUERY="search eventtype=splunkcraft2016 | timechart span=1d dc(player) AS player"
export CHART_2_ET="-7d@d"
export CHART_2_LT="-0d@d"
export CHART_2_SERIESFIELD="player"
export CHART_2_VALUEFIELD="player"
export CHART_2_COLOR="blue"
export CHART_2_TYPE="line"
export CHART_2_TITLE="Users last 7d"
export CHART_2_XOFFSET=0
export CHART_2_YOFFSET=0
export CHART_2_ZOFFSET=-80
export CHART_2_ORIENTATION=0
export CHART_2_MIRROR=1
export CHART_2_TIMER=60
export CHART_3_QUERY="search eventtype=splunkcraft2016 | stats count by player | sort limit=10 -count | eval player=substr(player, 1, 5)"
export CHART_3_SERIESFIELD="player"
export CHART_3_VALUEFIELD="count"
export CHART_3_ET="-7d@d"
export CHART_3_LT="-0d@d"
export CHART_3_COLOR="green"
export CHART_3_TYPE="pie"
export CHART_3_TITLE="Users last 7d"
export CHART_3_XOFFSET=-80
export CHART_3_YOFFSET=0
export CHART_3_ZOFFSET=0
export CHART_3_ORIENTATION=1
export CHART_3_MIRROR=0
export CHART_3_TIMER=60
export CHART_4_QUERY="search eventtype=splunkcraft2016 | stats dc(player) AS player"
# export CHART_4_QUERY="| stats count | eval player=2.0 | fields player"
export CHART_4_SERIESFIELD="player"
export CHART_4_VALUEFIELD="player"
export CHART_4_ET="-60m"
export CHART_4_LT="now"
export CHART_4_COLOR="black"
export CHART_4_TYPE="singlevalue"
export CHART_4_TITLE="Current Users"
export CHART_4_XOFFSET=80
export CHART_4_YOFFSET=0
export CHART_4_ZOFFSET=0
export CHART_4_ORIENTATION=1
export CHART_4_MIRROR=1
export CHART_4_TIMER=60