function requestHeaders(request) {
  return Object.fromEntries(
    Array.from(request.headers.entries(), ([key, value]) => [key.toLowerCase(), value])
  );
}

export async function onRequest(context) {
  const { handler } = await import("../../netlify/functions/api.mjs");
  const request = context.request;
  const body = request.method === "GET" || request.method === "HEAD"
    ? ""
    : await request.text();

  const result = await handler({
    httpMethod: request.method,
    rawUrl: request.url,
    path: new URL(request.url).pathname,
    headers: requestHeaders(request),
    body,
    env: context.env,
  });

  const responseHeaders = new Headers(result.headers || {});
  const responseBody = result.isBase64Encoded
    ? Uint8Array.from(atob(result.body || ""), (character) => character.charCodeAt(0))
    : (result.body || null);

  return new Response(responseBody, {
    status: result.statusCode || 200,
    headers: responseHeaders,
  });
}
