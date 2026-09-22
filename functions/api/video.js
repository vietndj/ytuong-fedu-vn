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
  headers.set('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)');

  let response = await fetch(driveUrl, {
    method: context.request.method,
    headers: headers,
    redirect: 'manual' // handle redirect manually to get the final download URL
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
  newHeaders.delete('content-disposition');
  newHeaders.set('access-control-allow-origin', '*');
  newHeaders.set('cross-origin-resource-policy', 'cross-origin');
  
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: newHeaders
  });
}
