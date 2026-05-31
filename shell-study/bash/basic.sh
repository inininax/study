#!/usr/local/bin/bash

### 선언
## #!/bin/bash
## #!/usr/local/bin/bash

### 참고
## https://wiki.kldp.org/HOWTO/html/Adv-Bash-Scr-HOWTO/
## http://www.tldp.org/LDP/Bash-Beginners-Guide/html/
## https://blog.gaerae.com/2015/01/bash-hello-world.html

### 선언
## #!/bin/bash
## #!/usr/bin/python
## #!/usr/bin/perl
## #!/usr/bin/php

### 선언 (동일)
## #!/usr/bin/env bash
## #!/usr/bin/env python
## #!/usr/bin/env perl
## #!/usr/bin/env php

### 매개 변수
## $0 : 실행된 스크립트 이름
## $1 : $1 $2 $3...${10}인자 순서대로 번호가 부여된다. 10번째부터는 "{}"감싸줘야 함
## $* : 전체 인자 값
## $@ : 전체 인자 값($* 동일하지만 쌍따옴표로 변수를 감싸면 다른 결과 나옴)
## $# : 매개 변수의 총 개수

### 변수
## ${변수} : $변수와 동일하지만 {} 사용해야만 동작하는 것들이 있음(예: echo ${string})
## ${변수:위치} : 위치 다음부터 문자열 추출(예: echo ${string:4})
## ${변수:위치:길이} : 위치 다음부터 지정한 길이 만큼의 문자열 추출(예: echo ${string:4:3})
## ${변수:-단어} : 변수 미선언 혹은 NULL일때 기본값 지정, 위치 매개 변수는 사용 불가(예: echo ${string:-HELLO})
## ${변수-단어} : 변수 미선언시만 기본값 지정, 위치 매개 변수는 사용 불가(예: echo ${string-HELLO})
## ${변수:=단어} : 변수 미선언 혹은 NULL일때 기본값 지정, 위치 매개 변수 사용 가능(예: echo ${string:=HELLO})
## ${변수=단어} : 변수 미선언시만 기본값 지정, 위치 매개 변수 사용 가능(예: echo ${string=HELLO})
## ${변수:?단어} : 변수 미선언 혹은 NULL일때 단어 출력 후 스크립트 종료,(예: echo ${string:?HELLO})
## ${변수?단어} : 변수 미선언시만 단어 출력 후 스크립트 종료(예: echo ${string?HELLO})
## ${변수:+단어} : 변수 선언시만 단어 사용(예: echo ${string:+HELLO})
## ${변수+단어} : 변수 선언 혹은 NULL일때 단어 사용(예: echo ${string+HELLO})
## ${#변수} : 문자열 길이(예: echo ${#string})
## ${변수#단어} : 변수의 앞부분부터 짧게 일치한 단어 삭제(예: echo ${string#a*b})
## ${변수##단어} : 변수의 앞부분부터 길게 일치한 단어 삭제(예: echo ${string##a*b})
## ${변수%단어} : 변수의 뒷부분부터 짧게 일치한 단어 삭제(예: echo ${string%b*c})
## ${변수%%단어} : 변수의 뒷부분부터 길게 일치한 단어 삭제(예: echo ${string%%b*c})
## ${변수/찾는단어/변경단어} : 처음 일치한 단어를 변경(예: echo ${string/abc/HELLO})
## ${변수//찾는단어/변경단어} : 일치하는 모든 단어를 변경(예: echo ${string//abc/HELLO})
## ${변수/#찾는단어/변경단어} : 앞부분이 일치하면 변경(예: echo ${string/#abc/HELLO})
## ${변수/%찾는단어/변경단어} : 뒷부분이 일치하면 변경(예: echo ${string/%abc/HELLO})
## ${!단어*}, ${!단어@} : 선언된 변수중에서 단어가 포함된 변수 명 추출(예: echo ${!string*}, echo ${!string@})

yesno="ABCDE0123456789"
echo "- "${yesno,,}   ## abcde0123456789 소문자로 변경

yesno=${yesno,,}
echo "- "$yesno       ## ABCDE0123456789
echo "- "${yesno}     ## ABCDE0123456789
echo "- "${yesno:0}   ## 0123456789
echo "- "${yesno:1}   ## 123456789
echo "- "${yesno:2}   ## 23456789
echo "- "${yesno:0:1} ## 0
echo "- "${yesno:2:1} ## 2
echo "- "${yesno:2:2} ## 23

string1="hello"
string2="world"
string3="!!"
if [ ${string1} == ${string2} ]; then
    # 실행 문장이 없으면 오류 발생함
    # 아래 echo 문장을 주석처리하면 확인 가능함
    echo "hello world"
elif [ ${string1} == ${string3} ]; then
    echo "hello world 2"
else
    echo "hello world 3"
fi