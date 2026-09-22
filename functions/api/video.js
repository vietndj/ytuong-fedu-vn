export async function onRequest(context) {
  const url = new URL(context.request.url);
  const id = url.searchParams.get('id');
  if (!id) return new Response('Missing id', { status: 400 });
  
  const driveUrl = `https://drive.google.com/uc?id=${id}&export=download`;
  
  const headers = new Headers();
  const range = context.request.headers.get('Range');
  if (range) {
      headers.set('Range', range);
  }
  headers.set('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');

  let response = await fetch(driveUrl, {
    method: context.request.method,
    headers: headers,
    redirect: 'manual'
  });
  
  if (response.status >= 300 && response.status < 400) {
      const location = response.headers.get('location');
      if (location) {
          response = await fetch(location, {
              method: context.request.method,
              headers: headers
          });
      }
  }

  const newHeaders = new Headers(response.headers);
  // Strip restrictive headers from Google Drive
  newHeaders.delete('content-disposition');
  newHeaders.delete('cross-origin-embedder-policy');
  newHeaders.delete('cross-origin-opener-policy');
  newHeaders.delete('cross-origin-resource-policy');
  newHeaders.delete('content-security-policy');
  newHeaders.delete('x-content-security-policy');
  newHeaders.delete('x-frame-options');

  // Set permissive CORS
  newHeaders.set('access-control-allow-origin', '*');
  newHeaders.set('X-Fedu-Proxy', 'v3');
  newHeaders.set('cross-origin-resource-policy', 'cross-origin');
  
  // Set aggressive edge caching for images/videos (Cloudflare will cache it for 1 year)
  newHeaders.set('cache-control', 'public, max-age=31536000, immutable');
  
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: newHeaders
  });
}
