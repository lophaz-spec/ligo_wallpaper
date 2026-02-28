import codecs
import re

file_path = "c:/Users/eloph/ligo_wallpaper/index.html"

with codecs.open(file_path, "r", "utf-8") as f:
    content = f.read()

supabase_script = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n    <script>'
if '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>' not in content:
    # find the last <script> tag before imagesData
    content = content.replace('<script>', supabase_script, 1)

new_functions = """
    const supabaseUrl = 'https://ubtagbxkbjmwwcblmfmb.supabase.co';
    const supabaseKey = 'sb_publishable_q6wT8LS6bT-4iM0Eonx3MA_6Hktkh0w';
    const supabaseClient = supabase.createClient(supabaseUrl, supabaseKey);

    async function updateDisplay() {
        try {
            const { count, error } = await supabaseClient
                .from('downloads')
                .select('*', { count: 'exact', head: true });
            
            if (!error && count !== null) {
                const totalCount = 1234 + count; // Retained the 1234 logic mentioned in instructions to be safe, or just count. The instructions said "1234부터 시작하지 않고 0부터 하려면 그냥 count만 넣으시면 됩니다". Let me check original code. Original code didn't add 1234, it just used the count. I will just use count.
                document.getElementById('downloadCount').innerText = count.toLocaleString();
            } else {
                console.error("Supabase error:", error);
            }
        } catch (e) {
            console.error(e);
        }
    }

    async function downloadCalendar() {
        const countSpan = document.getElementById('downloadCount');
        let currentText = countSpan.innerText.replace(/,/g, '');
        let count = parseInt(currentText) || 0;
        countSpan.innerText = (count + 1).toLocaleString();

        const downloadUrl = "./ligo_calendar_2026_adjusted.zip";
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = 'ligo_calendar_2026.zip';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        try {
            const { error } = await supabaseClient.from('downloads').insert([{}]);
            if (error) {
                console.error('다운로드 기록 실패:', error);
            }
        } catch(e) {
            console.error(e)
        }
    }
"""

# Replace the updateDisplay
content = re.sub(
    r'async function updateDisplay\(\)\s*\{[\s\S]*?(?=// 2\.)',
    new_functions + '\n\n          ',
    content
)

# Strip out the old downloadCalendar function until openGoogleForm
content = re.sub(
    r'async function downloadCalendar\(\)\s*\{[\s\S]*?(?=function openGoogleForm)',
    '',
    content
)

with codecs.open(file_path, "w", "utf-8") as f:
    f.write(content)

print("Patched successfully")
