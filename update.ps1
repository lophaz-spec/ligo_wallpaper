$htmlPath = "c:\Users\eloph\ligo_wallpaper\index.html"
$content = [System.IO.File]::ReadAllText($htmlPath, [System.Text.Encoding]::UTF8)

$content = $content.Replace('id="downloadCount">0</div>', 'id="downloadCount">6,250</div>')

$startToken = "async function updateDisplay() {"
$endToken = "function openGoogleForm() {"

$startIdx = $content.IndexOf($startToken)
$endIdx = $content.IndexOf($endToken)

if ($startIdx -ge 0 -and $endIdx -ge 0) {
    $preStart = $content.LastIndexOf("// 1.", $startIdx)
    if ($preStart -ge 0) {
        $startIdx = $preStart
    }

    $newJS = @"
// 1. 페이지 로드 시 현재 다운로드 횟수 가져오는 함수
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
        
        
"@

    $before = $content.Substring(0, $startIdx)
    $after = $content.Substring($endIdx)
    $newContent = $before + $newJS + $after

    [System.IO.File]::WriteAllText($htmlPath, $newContent, [System.Text.Encoding]::UTF8)
    Write-Host "Replacement successful."
} else {
    Write-Host "Cannot find markers."
}
