from fastapi import APIRouter

router = APIRouter(prefix = '/public', tags = ['Public'])


@router.get('/doctors')
async def doctors():
    pass


@router.get('/testimonials')
async def testimonial():
    pass


@router.post('/contact')
async def contact():
    pass
