// Cloudflare Pages Function: /api/edit
// Handles POST requests to update master_classifications.json via GitHub API

const REPO_OWNER = 'vietndj';
const REPO_NAME = 'ytuong-fedu-vn';
const FILE_PATH = 'master_classifications.json';

export async function onRequest(context) {
  const { request, env } = context;

  // CORS headers (cho phép gọi từ cùng domain + localhost dev)
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  try {
    const body = await request.json();
    const { password, entryKey, updates } = body;

    // 1. Validate password
    if (!password || password !== env.EDIT_PASSWORD) {
      return new Response(JSON.stringify({ error: 'Sai mật khẩu' }), {
        status: 403,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    if (!entryKey || !updates) {
      return new Response(JSON.stringify({ error: 'Thiếu entryKey hoặc updates' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    const githubToken = env.GITHUB_TOKEN;
    if (!githubToken) {
      return new Response(JSON.stringify({ error: 'Server thiếu GITHUB_TOKEN' }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    const branch = 'main';
    const apiBase = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}`;
    const headers = {
      'Authorization': `token ${githubToken}`,
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'ytuong-fedu-edit',
    };

    // 2. GET current file from GitHub (lấy SHA + content)
    const getRes = await fetch(`${apiBase}/contents/${FILE_PATH}?ref=${branch}`, { headers });
    if (!getRes.ok) {
      const errText = await getRes.text();
      return new Response(JSON.stringify({ error: `GitHub GET failed: ${getRes.status}`, detail: errText }), {
        status: 502,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    const fileData = await getRes.json();
    const sha = fileData.sha;

    // Decode base64 → parse JSON
    // GitHub returns base64 with newlines, handle both
    const rawContent = atob(fileData.content.replace(/\n/g, ''));
    const classifications = JSON.parse(rawContent);

    // 3. Tìm entry bằng entryKey (thử cả folder_name key lẫn shortcode match)
    let targetKey = null;
    if (classifications[entryKey]) {
      targetKey = entryKey;
    } else {
      // Tìm key chứa entryKey (shortcode match)
      for (const k of Object.keys(classifications)) {
        if (k.includes(entryKey) || (classifications[k].id && classifications[k].id.includes(entryKey))) {
          targetKey = k;
          break;
        }
      }
    }

    if (!targetKey) {
      return new Response(JSON.stringify({ error: `Không tìm thấy entry: ${entryKey}` }), {
        status: 404,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    const entry = classifications[targetKey];

    // 4. Apply updates
    if (updates.industry) {
      entry.industry = typeof updates.industry === 'string'
        ? { id: updates.industry.toLowerCase().replace(/[^a-z0-9]/g, '-'), name: updates.industry, icon: '🎯' }
        : updates.industry;
    }
    if (updates.shooting_style) {
      entry.shooting_style = typeof updates.shooting_style === 'string'
        ? { id: updates.shooting_style.toLowerCase().replace(/[^a-z0-9]/g, '-'), name: updates.shooting_style, icon: '🎬' }
        : updates.shooting_style;
    }
    if (updates.tech_tags) {
      entry.tech_tags = Array.isArray(updates.tech_tags) ? updates.tech_tags : updates.tech_tags.split(',').map(t => t.trim()).filter(Boolean);
    }
    if (updates.purpose !== undefined) {
      entry.purpose = updates.purpose;
    }
    if (updates.quick_takeaway !== undefined) {
      entry.quick_takeaway = updates.quick_takeaway;
    }
    if (updates.country) {
      entry.country = typeof updates.country === 'string'
        ? { id: updates.country.toLowerCase().replace(/[^a-z0-9]/g, '-'), name: updates.country, flag: '🌍', badge_color: 'gray' }
        : updates.country;
    }

    classifications[targetKey] = entry;

    // 5. Encode + PUT (commit to GitHub)
    const newContent = JSON.stringify(classifications, null, 2);
    // Use TextEncoder for proper UTF-8 → base64
    const uint8 = new TextEncoder().encode(newContent);
    let binary = '';
    for (let i = 0; i < uint8.length; i++) {
      binary += String.fromCharCode(uint8[i]);
    }
    const encoded = btoa(binary);

    const putRes = await fetch(`${apiBase}/contents/${FILE_PATH}`, {
      method: 'PUT',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: `[Edit] Cập nhật phân loại: ${targetKey}`,
        content: encoded,
        sha: sha,
        branch: branch,
      }),
    });

    if (!putRes.ok) {
      const errText = await putRes.text();
      return new Response(JSON.stringify({ error: `GitHub PUT failed: ${putRes.status}`, detail: errText }), {
        status: 502,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    const putData = await putRes.json();

    return new Response(JSON.stringify({
      success: true,
      message: `Đã cập nhật ${targetKey}`,
      commit: putData.commit ? putData.commit.sha.substring(0, 7) : 'unknown',
      updatedEntry: entry,
    }), {
      status: 200,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });

  } catch (err) {
    return new Response(JSON.stringify({ error: 'Server error', detail: err.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }
}
