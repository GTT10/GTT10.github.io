// ==========================================
// 統合JavaScript: 既存機能 + 新しいデザイン機能
// ==========================================

// スムーススクロール機能
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ヘッダーのスクロール効果
window.addEventListener('scroll', function() {
    const header = document.querySelector('.header');
    if (header && window.scrollY > 100) {
        header.style.backgroundColor = 'rgba(46, 134, 171, 0.95)';
        header.style.backdropFilter = 'blur(10px)';
    } else if (header) {
        header.style.backgroundColor = '#2E86AB';
        header.style.backdropFilter = 'none';
    }
});

// 科目カードのアニメーション設定
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// ページ読み込み時の初期化
document.addEventListener('DOMContentLoaded', function() {
    // 新しいデザインのアニメーション
    const cards = document.querySelectorAll('.subject-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });

    // 利用案内アイテムのアニメーション
    const aboutItems = document.querySelectorAll('.about-item');
    aboutItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(-30px)';
        item.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(item);
    });

    // 既存のタブ機能の初期化（後方互換性）
    initTabFunction();
});

// ==========================================
// 既存機能の保持（後方互換性）
// ==========================================

// タブ切り替え機能 (旧index.html用)
function initTabFunction() {
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.tab-content');

    // タブが存在する場合のみ実行
    if (tabs.length > 0 && contents.length > 0) {
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                // 現在アクティブなタブから'active'クラスを削除
                tabs.forEach(t => t.classList.remove('active'));
                // クリックされたタブに'active'クラスを追加
                tab.classList.add('active');

                // 現在アクティブなコンテンツから'active'クラスを削除
                contents.forEach(c => c.classList.remove('active'));
                // クリックされたタブのdata-target属性に対応するコンテンツに'active'クラスを追加
                const targetId = tab.dataset.target;
                const targetContent = document.getElementById(targetId);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
            });
        });
    }
}

// アコーディオン機能 (解説ページ用)
function toggleAccordion(id) {
    const accordion = document.getElementById(id);
    if (accordion) {
        const content = accordion.querySelector('.accordion-content');
        const arrow = accordion.querySelector('.accordion-arrow');
        
        if (content.style.display === 'none' || content.style.display === '') {
            content.style.display = 'block';
            if (arrow) arrow.style.transform = 'rotate(90deg)';
        } else {
            content.style.display = 'none';
            if (arrow) arrow.style.transform = 'rotate(0deg)';
        }
    }
}

// モバイルメニューの処理
function toggleMobileMenu() {
    const nav = document.querySelector('.nav');
    if (nav) {
        nav.classList.toggle('mobile-active');
    }
}
