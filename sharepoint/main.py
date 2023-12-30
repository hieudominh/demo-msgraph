import asyncio
import configparser
from loguru import logger
from msgraph.generated.models.o_data_errors.o_data_error import ODataError
from graph import Graph


async def main():
    # Load settings
    config = configparser.ConfigParser()
    config.read(["config.cfg", "config.dev.cfg"])
    graph: Graph = Graph(config)

    choice = -1

    while choice != 0:
        logger.info("Please choose one of the following options:")
        logger.info("0. Exit")
        logger.info("1. Search site")
        logger.info("2. get drives")
        logger.info("3. get drive root")
        logger.info("4. get items")

        try:
            choice = int(input())
        except ValueError:
            choice = -1

        try:
            if choice == 0:
                logger.info("Goodbye...")
            elif choice == 2:
                await get_drives(graph)
            elif choice == 1:
                await search_sharepoint_site(graph)
            elif choice == 4:
                await get_items(graph)
            elif choice == 3:
                await get_drive_root(graph)
            else:
                logger.warn("Invalid choice!\n")
        except ODataError as odata_error:
            logger.error("Error:")
            if odata_error.error:
                logger.error(odata_error.error.code, odata_error.error.message)


# </ProgramSnippet>


async def get_drives(graph: Graph):
    drives = await graph.get_drives(site_id=input("Enter site id: "))
    if drives:
        logger.info(str(drives))


async def get_items(graph: Graph):
    items = await graph.get_items(
        drive_id=input("Enter drive id: "), drive_item_id=input("Enter drive item id: ")
    )
    if items:
        logger.info(str(items))


async def get_drive_root(graph: Graph):
    items = await graph.get_drive_root(
        drive_id=input("Enter drive id: "),
    )
    if items:
        logger.info(str(items))


# <SearchSharepointSiteSnippet>
async def search_sharepoint_site(graph: Graph):
    site = await graph.search_sharepoint_site(keyword=input("Enter keyword: "))
    if site:
        logger.info("First site id found: " + str(site) + "\n")


# </SearchSharepointSiteSnippet>


# Run main
asyncio.run(main())
