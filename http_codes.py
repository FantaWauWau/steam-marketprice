# dict with http codes
# source: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

http_status_codes = {
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    103: "Early Hints",

    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi Status",
    208: "Already Reported",
    226: "IM Used",

    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See other",
    305: "Use Proxy",
    307: "Temporary Redirect",
    308: "Permanent Redirect",

    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not found",
    405: "Method not allowed",
    406: "Not acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Payload Too Large",
    414: "Request-URI Too Long",
    415: "Unsupported Media Type",
    416: "Requested Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",
    421: "Misdirected Request",
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    426: "Upgrade Required",
    428: "Precondition Required",
    429: "Too many requests",
    431: "Request Header Fields Too Large",
    444: "Connection closed without response",
    451: "Unavailable For Legal Reasons",
    499: "Client Closed Request",

    500: "Internal Server Error",
    501: "Not implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",
    507: "Insufficient Storage",
    508: "Loop Detected",
    510: "Not extended",
    511: "Network Authentication Required",
    599: "Network Connection Timeout Error"
}

http_status_description = {
    100: "The server has received the request headers and the client should proceed to send the request body.",
    101: "The requester has asked the server to switch protocols and the server has agreed to do so.",
    102: "A WebDAV request may contain many sub-requests involving file operations, requiring a long time to complete the request.",
    103: "Used to return some response headers before final HTTP message.",

    200: "Standard response for successful HTTP requests. The actual response will depend on the request method used.",
    201: "The request has been fulfilled, resulting in the creation of a new resource.",
    202: "The request has been accepted for processing, but the processing has not been completed. The request might or might not be eventually acted upon, and may be disallowed when processing occurs.",
    203: "The server is a transforming proxy (e.g. a Web accelerator) that received a 200 OK from its origin, but is returning a modified version of the origin's response.",
    204: "The server successfully processed the request, and is not returning any content.",
    205: "The server successfully processed the request, asks that the requester reset its document view, and is not returning any content.",
    206: "The server is delivering only part of the resource (byte serving) due to a range header sent by the client.",
    

}