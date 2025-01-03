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

async def process_data_line(line: str):
    await asyncio.sleep(random.uniform(0.01, 0.1))
    return f"Processed: {line.strip()}"

async def process_data_stream(filename="large_data.txt", chunk_size=1024):
    async with aiofiles.open(filename, 'r') as f:
        async for chunk in f:
            processed_chunk = await process_data_line(chunk)
            yield processed_chunk

async def main():
    start_time = time.time()
    await generate_large_data()

    print("\n--- Processing with Async Stream ---")
    async for processed_item in process_data_stream():
        print(processed_item)

    end_time = time.time()
    print(f"\nTotal processing time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())