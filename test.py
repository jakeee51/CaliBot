import asyncio, re

def edit_file(file, value):
   with open(file, 'r+') as f:
      lines = f.readlines()
      f.seek(0); found = False
      for line in lines:
         line = line.strip('\n')
         if str(line).lower() != str(value).lower():
            f.write(line + '\n')
         else:
            found = True
      f.truncate()
      return found

async def check_verify(record):
   while True:
      with open("verify.txt") as f:
         text = f.read()
         if not re.search(fr"{record}", text):
            break
      await asyncio.sleep(0)

async def main():
   try:
      await asyncio.wait_for(check_verify("123"), timeout=60) # Purge messages when record is removed from 'verify.txt' otherwise purge in 15 minutes
   except asyncio.TimeoutError:
      edit_file("verify.txt", f"123")

asyncio.run(main())
