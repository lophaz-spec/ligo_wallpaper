import codecs

file_path = r"c:\Users\eloph\ligo_wallpaper\index.html"
with codecs.open(file_path, "r", "utf-8") as f:
    content = f.read()

content = content.replace('id="downloadCount">0</div>', 'id="downloadCount">6,250</div>')

start_idx = content.find("async function updateDisplay() {")
end_idx = content.find("function openGoogleForm() {")

if start_idx != -1 and end_idx != -1:
    pre_start = content.rfind("// 1.", 0, start_idx)
    if pre_start != -1:
        start_idx = pre_start
    
    new_js = """// 1. 페이지 로드 시 현재 다운로드 횟수 가져오는 함수
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
            // ===== 다운로드 설정 =====
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
        
        """
    content = content[:start_idx] + new_js + content[end_idx:]
    with codecs.open(file_path, "w", "utf-8") as f:
        f.write(content)
    print("Successfully replaced.")
else:
    print("Markers not found.")
