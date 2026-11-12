// Asynchronous GPU -> CPU readback: readPixels into a fresh PIXEL_PACK_BUFFER behind a fence,
// collected by polling from the frame loop once the fence has signalled. Never blocks.
// (A fresh buffer each time: Chrome shadows READ buffers client-side and discards the shadow,
// with a warning, if one is rewritten.)
import { rawPassState } from './util.js';

export class Readback {
  constructor(gl) { this.gl = gl; this.queue = []; }

  // reads: [{ fb, attachment, x, y, w, h }] read in order into one buffer (RGBA_INTEGER/UNSIGNED_INT).
  // Returns the job; job.data (Uint32Array) is filled when poll() hands it back.
  start(reads, tag) {
    const gl = this.gl;
    const bytes = reads.reduce((a, r) => a + 16 * r.w * r.h, 0);
    rawPassState(gl);
    const pbo = gl.createBuffer();
    gl.bindBuffer(gl.PIXEL_PACK_BUFFER, pbo);
    gl.bufferData(gl.PIXEL_PACK_BUFFER, bytes, gl.STREAM_READ);
    let off = 0;
    for (const r of reads) {
      gl.bindFramebuffer(gl.FRAMEBUFFER, r.fb);
      gl.readBuffer(gl.COLOR_ATTACHMENT0 + (r.attachment || 0));
      gl.readPixels(r.x, r.y, r.w, r.h, gl.RGBA_INTEGER, gl.UNSIGNED_INT, off);
      off += 16 * r.w * r.h;
    }
    gl.readBuffer(gl.COLOR_ATTACHMENT0);
    gl.bindBuffer(gl.PIXEL_PACK_BUFFER, null);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    const job = { sync: gl.fenceSync(gl.SYNC_GPU_COMMANDS_COMPLETE, 0), pbo, bytes, tag, data: null };
    gl.flush();
    this.queue.push(job);
    return job;
  }

  get pending() { return this.queue.length; }

  // Completed jobs, in issue order (a job is only returned after all earlier ones).
  poll() {
    const gl = this.gl, done = [];
    while (this.queue.length) {
      const job = this.queue[0];
      if (gl.getSyncParameter(job.sync, gl.SYNC_STATUS) !== gl.SIGNALED) break;
      this.queue.shift();
      gl.deleteSync(job.sync);
      job.data = new Uint32Array(job.bytes / 4);
      gl.bindBuffer(gl.PIXEL_PACK_BUFFER, job.pbo);
      gl.getBufferSubData(gl.PIXEL_PACK_BUFFER, 0, job.data);
      gl.bindBuffer(gl.PIXEL_PACK_BUFFER, null);
      gl.deleteBuffer(job.pbo);
      done.push(job);
    }
    return done;
  }

  dispose() {
    for (const j of this.queue) { this.gl.deleteSync(j.sync); this.gl.deleteBuffer(j.pbo); }
    this.queue = [];
  }
}
