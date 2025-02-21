function hsvToRgb(h, s, v) {
    s /= 255;
    v /= 255;

    let c = v * s;
    let x = c * (1 - Math.abs((h / 60) % 2 - 1));
    let m = v - c;
    let r, g, b;

    if (0 <= h && h < 60) [r, g, b] = [c, x, 0];
    else if (60 <= h && h < 120) [r, g, b] = [x, c, 0];
    else if (120 <= h && h < 180) [r, g, b] = [0, c, x];
    else if (180 <= h && h < 240) [r, g, b] = [0, x, c];
    else if (240 <= h && h < 300) [r, g, b] = [x, 0, c];
    else [r, g, b] = [c, 0, x];

    r = Math.round((r + m) * 255);
    g = Math.round((g + m) * 255);
    b = Math.round((b + m) * 255);

    return `rgb(${r}, ${g}, ${b})`;
}

// Atualiza a cor do quadrado
function updateColor(boxId, hId, sId, vId) {
    const h = parseInt(document.getElementById(hId).value) || 0;
    const s = parseInt(document.getElementById(sId).value) || 0;
    const v = parseInt(document.getElementById(vId).value) || 0;

    const color = hsvToRgb(h, s, v);
    document.getElementById(boxId).style.backgroundColor = color;
}

// Inicializa os listeners
function initColorUpdate() {
    // Inputs Mínimos
    ['h_min', 's_min', 'v_min'].forEach(id => {
        document.getElementById(id).addEventListener('input', () => {
            updateColor('color_box_min', 'h_min', 's_min', 'v_min');
        });
    });

    // Inputs Máximos
    ['h_max', 's_max', 'v_max'].forEach(id => {
        document.getElementById(id).addEventListener('input', () => {
            updateColor('color_box_max', 'h_max', 's_max', 'v_max');
        });
    });

    // Atualiza inicialmente
    updateColor('color_box_min', 'h_min', 's_min', 'v_min');
    updateColor('color_box_max', 'h_max', 's_max', 'v_max');
}

document.addEventListener('DOMContentLoaded', initColorUpdate);
