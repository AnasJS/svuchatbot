from root import PreProcess, Steps


def main():
    pp = PreProcess(steps=[
        # Steps.READPSTFILE,
        # Steps.PARSEEMAILS
        # Steps.PARSEFROMFIELD,
        # Steps.PARSETOFIELD,
        # Steps.PARSESENTFIELD,
        # Steps.PARSESUBJECTFIELD,
        # Steps.PARSECCFIELD,
        # Steps.PARSEBCCFIELD,
        # Steps.PARSEDATEFIELD,
        Steps.PARSEBCCFIELD


    ])


    pp.run()


if __name__ == '__main__':
    main()
