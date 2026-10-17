/** Optional integration helpers; not loaded by the current game or gallery.
 * ctx must use native game pixels; images is Map-like object keyed by manifest id.
 * Load/decode PNGs before using this factory. The caller controls render order.
 */
export function createEnvironmentRenderer(ctx, manifest, images) {
  const assets = new Map(manifest.assets.map(asset => [asset.id, asset]));
  const animations = new Map(manifest.animations.map(animation => [animation.id, animation]));
  ctx.imageSmoothingEnabled = false;
  function draw(id, worldX, worldY, cameraX = 0, cameraY = 0) {
    const asset = assets.get(id), image = images[id];
    if (!asset || !image) return false;
    ctx.drawImage(image, Math.round(worldX - cameraX - asset.anchor[0]),
      Math.round(worldY - cameraY - asset.anchor[1]));
    return true;
  }
  function animated(animationId, seconds, x, y, cameraX = 0, cameraY = 0) {
    const animation = animations.get(animationId);
    if (!animation) return false;
    const index = Math.floor(Math.max(0, seconds) * animation.fps) % animation.frames.length;
    return draw(animation.frames[index], x, y, cameraX, cameraY);
  }
  function background(id, cameraX, viewportWidth, viewportHeight) {
    const asset = assets.get(id), image = images[id];
    if (!asset || !image || asset.category !== 'backgrounds') return false;
    const shift = ((cameraX * asset.parallax) % asset.width + asset.width) % asset.width;
    for (let x = -shift; x < viewportWidth; x += asset.width) {
      ctx.drawImage(image, Math.round(x), viewportHeight - asset.height);
    }
    return true;
  }
  return { draw, animated, background };
}

/** Stable terrain variants do not consume gameplay RNG (drops / shiny chance). */
export function tileVariant(tileX, tileY, count = 4) {
  if (!Number.isInteger(count) || count < 1) throw new RangeError('count must be a positive integer');
  return ((Math.imul(tileX + 17, 374761393) ^ Math.imul(tileY + 31, 668265263)) >>> 0) % count;
}
