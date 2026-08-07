function requestBody(request) {
  if (request.method === "GET" || request.method === "HEAD") return "";
  if (typeof request.body === "string") return request.body;
  if (request.body == null) return "";
  return JSON.stringify(request.body);
}

function apiPath(request) {
  const route = request.query && request.query.path;
  const value = Array.isArray(route) ? route.join("/") : String(route || "");
  return `/api${value ? `/${value.replace(/^\/+/, "")}` : ""}`;
}

function requestUrl(request, path) {
  const protocol = request.headers["x-forwarded-proto"] || "https";
  const host = request.headers["x-forwarded-host"] || request.headers.host || "localhost";
  return `${protocol}://${host}${path}`;
}

export default async function vercelHandler(request, response) {
  try {
    const { handler } = await import("../netlify/functions/api.mjs");
    const path = apiPath(request);
    const result = await handler({
      httpMethod: request.method,
      rawUrl: requestUrl(request, path),
      path,
      headers: request.headers,
      body: requestBody(request),
      env: process.env,
    });

    Object.entries(result.headers || {}).forEach(([name, value]) => {
      response.setHeader(name, value);
    });

    const body = result.isBase64Encoded
      ? Buffer.from(result.body || "", "base64")
      : result.body || "";

    response.status(result.statusCode || 200).send(body);
  } catch (error) {
    console.error("Vercel API invocation failed", error);
    response.status(500).json({ error: "The server could not process this request." });
  }
}
