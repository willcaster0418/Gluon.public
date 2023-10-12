export PYTHONPATH=$PYTHONPATH:/gluon
export PS1="\[\033[0;32m\]\u@\h:\w \$\[\033[0m\] "
export LC_ALL=ko_KR.UTF-8
export PYTHONENCODING=utf-8

export MW_URL='127.0.0.1'
export MW_PORT=60000

export MEMORY_UNIT=1472
alias ls='ls -aF --color=auto'
alias psg='ps aux|grep -v grep|grep '
alias cdbatch='cd /gluon/run/batch'
alias cdlog='cd /gluon/log'
alias cdFMS='cd /gluon/run/daemon/FMS'
alias cdrun='cd /gluon/run'
alias cdconfig='cd /gluon/config'
set -o vi