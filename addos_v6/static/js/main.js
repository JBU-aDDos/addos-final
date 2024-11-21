(function () {
  'use strict';

  const $body = document.querySelector('body');

  // 페이지 로드 시 초기 애니메이션 재생.
  window.addEventListener('load', () => {
    setTimeout(() => {
      $body.classList.remove('is-preload');
    }, 100);
  });

  // 슬라이드쇼 배경.
  function initSlideshow(settings) {
    let pos = 0;
    const $wrapper = document.createElement('div');
    $wrapper.id = 'bg';
    $body.appendChild($wrapper);

    const $bgs = Object.keys(settings.images).map((key) => {
      const $bg = document.createElement('div');
      $bg.style.backgroundImage = `url("${key}")`;
      $bg.style.backgroundPosition = settings.images[key];
      $wrapper.appendChild($bg);
      return $bg;
    });

    if ($bgs.length === 0) return;

    $bgs[pos].classList.add('visible', 'top');

    if ($bgs.length === 1 || !canUse('transition')) return;

    setInterval(() => {
      const lastPos = pos;
      pos = (pos + 1) % $bgs.length;

      $bgs[lastPos].classList.remove('top');
      $bgs[pos].classList.add('visible', 'top');

      setTimeout(() => {
        $bgs[lastPos].classList.remove('visible');
      }, settings.delay / 2);
    }, settings.delay);
  }

  // 배경 변경 기능
  function changeBackground() {
    const images = document.querySelectorAll('#bg .bg-image'); // 배경 이미지를 담은 div들 선택
    let currentIndex = 0;

    function updateBackground() {
      images[currentIndex].classList.remove('visible'); // 현재 이미지의 visible 클래스를 제거
      currentIndex = (currentIndex + 1) % images.length; // 다음 이미지 인덱스를 계산
      images[currentIndex].classList.add('visible'); // 다음 이미지에 visible 클래스 추가
    }

    setInterval(updateBackground, 3000); // 3초마다 배경 이미지 변경
  }

  // 슬라이드쇼 설정
  const slideshowSettings = {
    images: {
      '{% static "img/bg01.jpg" %}': 'center',
      '{% static "img/bg02.jpg" %}': 'center',
      '{% static "img/bg03.jpg" %}': 'center',
    },
    delay: 6000,
  };

  // 슬라이드쇼 초기화
  initSlideshow(slideshowSettings);
  changeBackground(); // 배경 이미지 변경 시작

  // // 회원가입 폼 처리
  // function handleSignupForm() {
  //     const $form = document.querySelector('#signup-form');
  //     if (!$form) return;
  //     const $submit = $form.querySelector('input[type="submit"]');
  //     const $message = document.createElement('span');
  //     $message.classList.add('message');
  //     $form.appendChild($message);

  //     const showMessage = (type, text) => {
  //         $message.textContent = text;
  //         $message.classList.add(type, 'visible');
  //         setTimeout(() => {
  //             $message.classList.remove('visible');
  //         }, 3000);
  //     };

  //     $form.addEventListener('submit', event => {
  //         event.preventDefault();
  //         $message.classList.remove('visible');
  //         $submit.disabled = true;

  //         // 실제 AJAX 요청을 구현해야 함
  //         setTimeout(() => {
  //             $form.reset();
  //             $submit.disabled = false;
  //             showMessage('success', '감사합니다!');
  //             // 실패 시: showMessage('failure', '문제가 발생했습니다. 다시 시도해 주세요.');
  //         }, 750);
  //     });
  // }

  // // 폼 처리 초기화
  // handleSignupForm();

  // 유틸리티 함수
  function canUse(property) {
    const div = document.createElement('div');
    const up = property.charAt(0).toUpperCase() + property.slice(1);
    return (
      property in div.style ||
      `Moz${up}` in div.style ||
      `Webkit${up}` in div.style ||
      `O${up}` in div.style ||
      `ms${up}` in div.style
    );
  }
})();
