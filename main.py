import asyncio
import time

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel


class CalculateRequest(BaseModel):
    numbers: list[int]
    delays: list[float]


class NumberResult(BaseModel):
    number: int
    square: int
    delay: float
    time: float


class CalculateResponse(BaseModel):
    results: list[NumberResult]
    total_time: float
    parallel_faster_than_sequential: bool


async def calculate_square(number: int, delay: float) -> NumberResult:
    start = time.perf_counter()

    await asyncio.sleep(delay)

    square = number * number
    end = time.perf_counter()
    elapsed = round(end - start, 2)
    return NumberResult(
        number=number,
        square=square,
        delay=delay,
        time=elapsed
    )


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.post("/calculate/", response_model=CalculateResponse)
async def calculate(request: CalculateRequest):
    if len(request.numbers) != len(request.delays):
        raise HTTPException(
            status_code=400,
            detail="Количество чисел и задержек должно совпадать"
        )

    start = time.perf_counter()
    tasks = []

    for n, d in zip(request.numbers, request.delays):
        res = calculate_square(n, d)
        tasks.append(res)

    results = await asyncio.gather(*tasks)

    end = time.perf_counter()
    sequential_time = sum(request.delays)
    parallel_time = round(end - start, 2)
    is_faster = sequential_time > parallel_time

    return CalculateResponse(
        results=results,
        total_time=parallel_time,
        parallel_faster_than_sequential=is_faster
    )
