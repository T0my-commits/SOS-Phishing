export function debugPrint(caller, msg) {
    const PADDING =35;
    const PREFIX = "[DEBUG] ";
    const curr_padding = caller.length + PREFIX.length + 2;
    const dots = '.'.repeat(Math.max(0, PADDING - curr_padding));

    if (useRuntimeConfig().public.debug) {
        console.debug(`${PREFIX}{${caller}}: ${msg}`);
    }
}
