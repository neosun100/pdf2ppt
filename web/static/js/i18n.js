// i18n translations
const translations = {
    'en': {
        'upload.title': 'Drop PDF files here or click to browse',
        'upload.subtitle': 'Support single or multiple PDF files',
        'upload.button': 'Select Files',
        'options.title': 'Conversion Options',
        'options.pages': 'Page Range',
        'options.parallel': 'Parallel Workers',
        'options.force': 'Force Overwrite',
        'options.keepTemp': 'Keep Temporary Files',
        'files.title': 'Files to Convert',
        'files.convert': '🚀 Start Conversion',
        'progress.title': 'Conversion Progress',
        'results.title': 'Conversion Results',
        'star.text': 'Enjoying PDF2PPT? Give us a star on GitHub!',
        'star.link': 'Star on GitHub →'
    },
    'zh-CN': {
        'upload.title': '拖放 PDF 文件到这里或点击浏览',
        'upload.subtitle': '支持单个或多个 PDF 文件',
        'upload.button': '选择文件',
        'options.title': '转换选项',
        'options.pages': '页面范围',
        'options.parallel': '并行线程数',
        'options.force': '强制覆盖',
        'options.keepTemp': '保留临时文件',
        'files.title': '待转换文件',
        'files.convert': '🚀 开始转换',
        'progress.title': '转换进度',
        'results.title': '转换结果',
        'star.text': '喜欢 PDF2PPT？给我们一个 Star 吧！',
        'star.link': '前往 GitHub →'
    },
    'zh-TW': {
        'upload.title': '拖放 PDF 檔案到這裡或點擊瀏覽',
        'upload.subtitle': '支援單個或多個 PDF 檔案',
        'upload.button': '選擇檔案',
        'options.title': '轉換選項',
        'options.pages': '頁面範圍',
        'options.parallel': '並行執行緒數',
        'options.force': '強制覆蓋',
        'options.keepTemp': '保留暫存檔案',
        'files.title': '待轉換檔案',
        'files.convert': '🚀 開始轉換',
        'progress.title': '轉換進度',
        'results.title': '轉換結果',
        'star.text': '喜歡 PDF2PPT？給我們一個 Star 吧！',
        'star.link': '前往 GitHub →'
    },
    'ja': {
        'upload.title': 'PDFファイルをドロップまたはクリックして選択',
        'upload.subtitle': '単一または複数のPDFファイルをサポート',
        'upload.button': 'ファイルを選択',
        'options.title': '変換オプション',
        'options.pages': 'ページ範囲',
        'options.parallel': '並列ワーカー数',
        'options.force': '強制上書き',
        'options.keepTemp': '一時ファイルを保持',
        'files.title': '変換するファイル',
        'files.convert': '🚀 変換開始',
        'progress.title': '変換進行状況',
        'results.title': '変換結果',
        'star.text': 'PDF2PPTが気に入りましたか？GitHubでスターをください！',
        'star.link': 'GitHubへ →'
    }
};

let currentLang = 'en';

function changeLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('language', lang);
    updateTexts();
}

function updateTexts() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[currentLang] && translations[currentLang][key]) {
            el.textContent = translations[currentLang][key];
        }
    });
}

// Initialize language
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('language') || 'en';
    document.getElementById('language').value = savedLang;
    changeLanguage(savedLang);
});
