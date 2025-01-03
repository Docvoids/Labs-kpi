import asyncio
import aiofiles
import random
import time

async def generate_large_data(filename="large_data.txt", num_lines=1000):
    async with aiofiles.open(filename, 'w') as f:
        for i in range(num_lines):
            data = f"Data line {i}: {random.randint(0, 1000)}\n"
            await f.write(data)
    print(f"Generated {filename} with {num_lines} lines.")

async def main():
    start_time = time.time()
    await generate_large_data()
    end_time = time.time()
    print(f"\nData generation time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())