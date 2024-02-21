# queue_manager.py

async def list_queue(ctx, queue_list):
    if ctx.guild.id in queue_list and queue_list[ctx.guild.id]:
        queue_info = "Очередь треков:\n"
        for title in queue_list[ctx.guild.id]:
            queue_info += f"- {title}\n"
        await ctx.send(queue_info)
    else:
        await ctx.send("Очередь пуста.")