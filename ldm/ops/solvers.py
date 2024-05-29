import torch
from tqdm.auto import trange

__all__ = ['sample_ddim', 'sample_euler']


@torch.no_grad()
def sample_ddim(noise, model, sigmas, eta=0., show_progress=True):
    """DDIM solver steps."""
    x = noise
    for i in trange(len(sigmas) - 1, disable=not show_progress):
        denoised = model(x, sigmas[i])
        noise_factor = eta * (sigmas[i + 1]**2 / sigmas[i]**2 *
                              (1 - (1 - sigmas[i]**2) /
                               (1 - sigmas[i + 1]**2)))
        d = (x - (1 - sigmas[i]**2)**0.5 * denoised) / sigmas[i]
        x = (1 - sigmas[i + 1] ** 2) ** 0.5 * denoised + \
            (sigmas[i + 1] ** 2 - noise_factor ** 2) ** 0.5 * d
        if sigmas[i + 1] > 0:
            x += noise_factor * torch.randn_like(x)
    return x

@torch.no_grad()
def sample_euler(noise, model, sigmas, show_progress=True):
    """Euler steps."""
    x = noise
    for i in trange(len(sigmas) - 1, disable=not show_progress):
        denoised = model(x, sigmas[i])
        step_size = sigmas[i + 1] - sigmas[i]
        x = x + step_size * denoised
        if sigmas[i + 1] > 0:
            x += sigmas[i + 1] * torch.randn_like(x)
    return x