import ast
import sys
import html
import inspect
import traceback
from pyrogram import Client, filters


def memory_file(name=None, contents=None, *, bytes=True):
    if isinstance(contents, str) and bytes:
        contents = contents.encode()
    file = BytesIO() if bytes else StringIO()
    if name:
        file.name = name
    if contents:
        file.write(contents)
        file.seek(0)
    return file

async def run_code(client, message):
    class UniqueExecReturnIdentifier:
        pass
    code = message.text[5:].strip()
    if not code:
        await message.reply_text('code 100')
        return
    tree = ast.parse(code)
    obody = tree.body
    body = obody.copy()
    body.append(ast.Return(ast.Name('_ueri', ast.Load())))
    def _gf(body):
        # args: m, message, c, client, _ueri
        func = ast.AsyncFunctionDef('ex', ast.arguments([], [ast.arg(i, None, None) for i in ['m', 'message', 'c', 'client', '_ueri']], None, [], [], None, []), body, [], None, None)
        ast.fix_missing_locations(func)
        mod = ast.parse('')
        mod.body = [func]
        fl = locals().copy()
        exec(compile(mod, '<ast>', 'exec'), globals(), fl)
        return fl['ex']
    try:
        exx = _gf(body)
    except SyntaxError as ex:
        if ex.msg != "'return' with value in async generator":
            raise
        exx = _gf(obody)
    escaped_code = html.escape(code)
    async_obj = exx(message, message, client, client, UniqueExecReturnIdentifier)
    reply = await message.reply_text('Type[py]\n<code>{}</code>\nState[Executing]'.format(escaped_code))
    stdout = sys.stdout
    stderr = sys.stderr
    wrapped_stdout = memory_file(bytes=False)
    wrapped_stdout.buffer = memory_file()
    wrapped_stderr = memory_file(bytes=False)
    wrapped_stderr.buffer = memory_file()
    sys.stdout = wrapped_stdout
    sys.stderr = wrapped_stderr
    try:
        if inspect.isasyncgen(async_obj):
            returned = [i async for i in async_obj]
        else:
            returned = [await async_obj]
            if returned == [UniqueExecReturnIdentifier]:
                returned = []
    except Exception:
        await message.reply_text(traceback.format_exc(), parse_mode=None)
        return
    finally:
        sys.stdout = stdout
        sys.stderr = stderr
    wrapped_stdout.seek(0)
    wrapped_stderr.seek(0)
    wrapped_stdout.buffer.seek(0)
    wrapped_stderr.buffer.seek(0)
    r = []
    outtxt = wrapped_stderr.read() + wrapped_stderr.buffer.read().decode()
    if outtxt.strip().strip('\n').strip():
        r.append(outtxt)
    errtxt = wrapped_stdout.read() + wrapped_stdout.buffer.read().decode()
    if errtxt.strip().strip('\n').strip():
        r.append(errtxt)
    r.extend(returned)
    r = [html.escape(str(i).strip('\n')) for i in r]
    r = '\n'.join([f'<code>{i}</code>' for i in r])
    r = r.strip() or 'undefined'
    await reply.edit_text('<b>Type[py]</b>\n<code>{}</code>\nState[Executed]\n<b>Output</b>\n{}'.format(escaped_code, r))
