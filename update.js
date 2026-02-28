const fs = require('fs');

const filePath = 'c:\\Users\\eloph\\ligo_wallpaper\\index.html';
let content = fs.readFileSync(filePath, 'utf8');

content = content.replace('id="downloadCount">0</div>', 'id="downloadCount">6,250</div>');

let startIdx = content.indexOf('async function updateDisplay() {');
let endIdx = content.indexOf('function openGoogleForm() {');

if (startIdx !== -1 && endIdx !== -1) {
    let preStart = content.lastIndexOf('// 1.', startIdx);
    if (preStart !== -1) {
        startIdx = preStart;
    }

    let newJs = `// 1. 페이지 로드 시 현재 다운로드 횟수 가져오는 함수
        let currentDownloadCount = 6250;

        async function updateDisplay() {
            const storedCount = localStorage.getItem('downloadCount');
            if (storedCount) {
                currentDownloadCount = parseInt(storedCount, 10);
            } else {
                currentDownloadCount = 6250;
            }
            document.getElementById('downloadCount').innerText = currentDownloadCount.toLocaleString();
        }

        // 2. 다운로드 버튼 클릭 시 숫자 1 올리는 함수
        async function downloadCalendar() {
            // ===== 다운로드 경로 설정 =====
            const downloadUrl = "./ligo_calendar_2026_adjusted.zip";
            
            // ===== 다운로드 실행 =====
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = 'ligo_calendar_2026.zip';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // ===== 카운트 증가 =====
            currentDownloadCount++;
            localStorage.setItem('downloadCount', currentDownloadCount.toString());
            document.getElementById('downloadCount').innerText = currentDownloadCount.toLocaleString();
        }
        
        `;

    content = content.substring(0, startIdx) + newJs + content.substring(endIdx);
    fs.writeFileSync(filePath, content, 'utf8');
    console.log('Successfully replaced.');
} else {
    console.log('Markers not found.');
}
