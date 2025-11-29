class ThemeManager {
    constructor() {
        this.themes = ['light', 'dark', 'nature', 'ocean'];
        this.currentTheme = this.getStoredTheme() || 'light';
        this.themeLink = null;
        this.init();
    }

    init() {
        this.loadTheme(this.currentTheme);
        this.bindEvents();
    }

    getStoredTheme() {
        return localStorage.getItem('theme');
    }

    setStoredTheme(theme) {
        localStorage.setItem('theme', theme);
    }

    loadTheme(themeName) {
        // Удаляем ВСЕ предыдущие темы
    document.querySelectorAll('link[data-theme]').forEach(link => link.remove());

    // Загружаем выбранную тему (кроме светлой - она базовая)
    if (themeName !== 'light') {
        const themeLink = document.createElement('link');
        themeLink.rel = 'stylesheet';
        themeLink.href = `/static/css/themes/${themeName}-theme.css`;
        themeLink.setAttribute('data-theme', themeName); // Добавляем атрибут для идентификации
        document.head.appendChild(themeLink);
    }

    // Устанавливаем атрибут data-theme
    document.documentElement.setAttribute('data-theme', themeName);
        this.currentTheme = themeName;
        this.setStoredTheme(themeName);
        
        // Обновляем активный элемент в dropdown
        this.updateActiveTheme(themeName);
    }

    bindEvents() {
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('theme-option')) {
                e.preventDefault();
                const theme = e.target.dataset.theme;
                this.loadTheme(theme);
                this.showThemeNotification(theme);
            }
        });
    }

    updateActiveTheme(themeName) {
        // Убираем активный класс у всех опций
        document.querySelectorAll('.theme-option').forEach(option => {
            option.classList.remove('active');
        });
        
        // Добавляем активный класс к выбранной теме
        const activeOption = document.querySelector(`.theme-option[data-theme="${themeName}"]`);
        if (activeOption) {
            activeOption.classList.add('active');
        }
    }

    showThemeNotification(theme) {
        const themeNames = {
            'light': 'Светлая',
            'dark': 'Тёмная', 
            'nature': 'Природа',
            'ocean': 'Океан'
        };

        // Создаем toast уведомление
        const toastHtml = `
            <div class="toast align-items-center text-white bg-primary border-0 show position-fixed" 
                 style="bottom: 20px; right: 20px; z-index: 1050;">
                <div class="d-flex">
                    <div class="toast-body">
                        Тема изменена: ${themeNames[theme]}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', toastHtml);
        
        // Удаляем toast через 3 секунды
        setTimeout(() => {
            const toasts = document.querySelectorAll('.toast');
            toasts.forEach(t => t.remove());
        }, 3000);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});