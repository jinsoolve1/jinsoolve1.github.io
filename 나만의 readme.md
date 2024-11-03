---
last_modified_at: 2024-08-01
---
# Posting

1. _ posts/YYYY-MM-DD-(나만의-제목) 이런식으로 포스팅한다.
2. title : 말 그대로 제목 블로그에서는 .md파일의 제목이 아닌 title에 넣은 값이 제목이다
3. excerpt: 포스트 글을 미리 볼 때 밑의 작은 설명 글이다.
4. categoreis: 어느 카테고리에 넣을 지 정함
5. tags: 해당 글의 태그들을 달음
6. permalink: 내부의 링크로 해당 링크로 주소가 나타난다. 
	ex) jinsoolve.github.io/permalink/,,, 이런식으로
7. toc: 우측에 목차 네비게이션 (Table of content)
8. toc_sticky: 본문 목차 네비게이션 고정 여부
9. date: 처음 포스팅한 날짜 YYYY-MM-DD 형식
10. last_modified_at: 가장 최근에 수정한 날짜. 마찬가지로 YYYY-MM-DD 형식

## 이미지 첨부
포스팅에서 이미지를 첨부할 때, 기본적으로 아무 위치에나 넣어도 되지만 경로의 맨 앞에는 '/'가 있어야 한다.

---

# Category
카테고리를 추가하려면 다음과 같다.
1. _ pages/categories/ 하위에 category-(카테고리이름).md 를 추가한다.
	아래와 같이 title과 permalink, taxonomy 를 수정해준다.
	taxonomy는 title과 같이 하면 된다.
	```
	title: "Categories1" # 카테고리 이름(수정할 것)
	layout: category
	permalink: /categories/categories1/ # url(수정할 것)
	author_profile: true
	taxonomy: Categories1(수정할 것)
	sidebar:
	nav: "categories"
	```
2. _ data/navigation.yml 파일에 title과 url을 만든다.
	이때, title과 url이 1.에서 했던 title과 permalink와 각각 같아야 한다.

---
# 폰트

## 폰트 바꾸기
1. /assets/css/main.scss에서 web font를 가지고 온다. 
2. /\_sass/minimal-mistakes/\_variables.scss 으로 이동해서  
   /* system typefaces \*/  
   $serif: Georgia, Times, serif !default;  
   /* 2022.01.19 font change */   
   $sans-serif: "ONE-Mobile-Regular",  
	위 sans-serif의 값을 수정한다.

## 폰트 크기 바꾸기
1. /\_sass/minimal-mistakes/\_reset.scss 으로 이동해서 바꾼다. 특히 medium이 많이 쓰이는 듯 하다.

---
# 글의 좌우 폭 너비 조정하기
1. \_sass_minimal-mistakes_variables.scss을 본다
2. \$x-large: 1400px !default;  
   $max-width: $x-large !default;
3. 위 같은 코드가 있는데 max-width를 조정해줘야 최대 너비가 변화한다.   
4. 이때 x-large변수를 사용하므로 이를 변화시켜주면 된다.

---
# 수식 블록 조정
1. \_layouts/deafult.html에 `{% include mathjax_support.html %}` 넣기
2. \_includes/mathjax_support.html에 아래 코드 넣기
	```html
	<script type="text/x-mathjax-config">  
	    MathJax.Hub.Config({  
	        extensions: ["tex2jax.js"],  
	        jax: ["input/TeX", "output/HTML-CSS"],  
	        tex2jax: {  
	            inlineMath: [ ['$','$'], ["\\(","\\)"] ],  
	            displayMath: [ ['$$','$$'], ["\\[","\\]"] ],  
	            processEscapes: true  
	        },  
	  
	        "HTML-CSS": {  
	            availableFonts: ["TeX"],  
	            linebreaks: {  
	                automatic: true  
	            }  
	        }  
	    });  
	  
	    let initialWidth = window.innerWidth;  
	    window.addEventListener('resize', MJrerender);  
	    let t = -1;  
	    let delay = 250;  
	  
	    function MJrerender() {  
	      // Check if the width has actually changed  
	      if (window.innerWidth === initialWidth) {  
	        return;  
	      }  
	  
	      initialWidth = window.innerWidth;  
	  
	      if (t >= 0) {  
	        // If we are still waiting, then the user is still resizing =>  
	        // postpone the action further!  
	        window.clearTimeout(t);  
	      }  
	      t = window.setTimeout(function() {  
	        MathJax.Hub.Queue(["Rerender",MathJax.Hub]);  
	        t = -1; // Reset the handle  
	      }, delay);  
	    }  
	</script>  
	  
	<script type="text/javascript"  
	        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-AMS_HTML-full,Safe,https://DOMAIN/config.js">  
	</script>  
	<script type="text/javascript" id="MathJax-script" async  
	        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">  
	</script>
	```
	- linebreaks의 automatic: true가 inline 수식 블록을 line break해준다.
	- version3가 인라인 수식을 안 먹어서 version2.7.5도 같이 넣어줬다.
	- version3에서 수식 블록의 가로스크롤이 가능해졌다.
	- 윈도우 크기가 resize 될 때마다 rerender 할 수 있도록 설정했다. delay의 값을 100ms으로 해서 해당 delay 후 새로고침된다. delay 값을 키울 수록 더 늦게 새로고침된다.
	- 모바일 화면에서 위 아래로 스크롤 할 때 주소표시줄이나 툴바가 나타나면서 화면 위아래 크기가 resize돼서 스크롤 할 때마다 수식블록이 resize 되는 문제가 생겼다. 이를 가로화면의 너비가 변화할 때만 rerender 하는 방식으로 처리해서 해결했다.
1. 수식 블록의 가로스크롤을 위해서는 \_base.scss 에서 mjx-container {} 를 수정해줬더니 해결됐다.
	```scss
	mjx-container {  
	  display: block;  
	  overflow-x: auto;  
	  overflow-y: hidden;  
	  max-width: 100%;  
	}
	```


---
# 헤더 스크롤 시 숨겼다 나왔다 시키기
1. \_masthead.scss에서 hidden 속성을 만들었다.
2. \_includes/head/custom.html에 script 코드를 넣었다.

---
# 사이드바 하위 목록
1. \_includes > nav_list를 수정한다.

---
# Tags, Categories 위치 header 쪽으로 변경
1. page__taxonomy.html에서 해당 내용을 생성
2. single.html과 gallery.html에서 page__taxonomy.html파일을 사용. 여기서 위치를 footer에서 꺼내서 header 안으로 넣어줌.
3. _page.scss에서 .page__taxonomy 내용을 수정해서 css를 수정함.


---
# 추가 사항
- manifest가 계속 현재 경로에서 찾아서 custom.html에서 ../../을 앞에 추가해주었더니 정상 동작했다.  
- theme가 적용이 안 돼서 찾아보니 \_base.scss의 106, 121줄을 주석처리 했더니 해결됐다.
- Chrome 기반에서 사이드목차의 링크 색깔이 자꾸 변하는 문제가 있어서 \_navigation.scss 파일의 .toc 내용을 수정했다.

