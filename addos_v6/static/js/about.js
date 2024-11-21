(function() {
    "use strict";

    /**
     * 카드 콘텐츠 토글 기능
     * @param {HTMLElement} header - 클릭된 카드 헤더 요소
     */
    function toggleCard(header) {
        const card = header.parentElement; // 카드 요소 가져오기
        const content = card.querySelector('.card-content'); // 카드 콘텐츠 요소 가져오기
        const icon = header.querySelector('.toggle-icon'); // 토글 아이콘 요소 가져오기

        const isActive = header.classList.contains('active'); // 현재 활성화 상태 확인

        if (!isActive) {
            header.classList.add('active'); // 활성화 클래스 추가
            header.setAttribute('aria-expanded', 'true'); // ARIA 속성 업데이트
            icon.textContent = '−'; // 아이콘 변경
            content.classList.add('active'); // 콘텐츠 활성화
        } else {
            header.classList.remove('active'); // 활성화 클래스 제거
            header.setAttribute('aria-expanded', 'false'); // ARIA 속성 업데이트
            icon.textContent = '+'; // 아이콘 변경
            content.classList.remove('active'); // 콘텐츠 비활성화
        }
    }

    // 전역 함수로 toggleCard 등록
    window.toggleCard = toggleCard;

    // 키보드 이벤트 처리 (Enter, Space 키로 카드 토글)
    document.querySelectorAll('.card-header').forEach(header => {
        header.addEventListener('keypress', function(event) {
            if (event.key === 'Enter' || event.key === ' ') {
                toggleCard(this);
                event.preventDefault();
            }
        });
    });

})();
