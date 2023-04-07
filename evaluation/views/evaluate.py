from evaluation.views.utils import *


class EvaluateView:
    @staticmethod
    @api_view(['POST'])
    def evaluate(request, format=None):
        body = load_request_body(request)
        result = Evaluate.evaluate(body)
        json_response = [r.__dict__ for r in result]
        return JsonResponse(json_response, safe=False)

    @staticmethod
    @api_view(['POST'])
    def compare(request, format=None):
        body = load_request_body(request)
        result = Compare.compare(body)
        json_response = result.__dict__
        return JsonResponse(json_response, safe=False)

    @staticmethod
    @api_view(['GET'])
    def evaluate1(request):
        result = [
            {
                "name": "Atadi",
                "totalCycleTime": 110.425,
                "totalCost": 8.834,
                "unitCost": [
                    {
                        "lane": "Customer Service Department",
                        "cost": 0.08
                    },
                    {
                        "lane": "Finance Department",
                        "cost": 0.08
                    }
                ],
                "transparency": [
                    {
                        "view": "Customer Service Department View",
                        "numberOfExplicitTask": 4,
                        "transparency": 0.308
                    },
                    {
                        "view": "Finance Department View",
                        "numberOfExplicitTask": 4,
                        "transparency": 0.308
                    },
                    {
                        "view": "Customer View",
                        "numberOfExplicitTask": 5,
                        "transparency": 0.384
                    }
                ],
                "totalNumberExplicitTasks": 13,
                "quality": 0.76,
                "numberOfOptionalTasks": 3,
                "totalTasks": 13,
                "flexibility": 0.2307,
                "handledTasks": 0,
                "unHandledTasks": 0,
                "exceptionHandling": 1
            }
        ]

        return JsonResponse(result, safe=False)

    @ staticmethod
    @ api_view(['GET'])
    def evaluate2(request):
        result = [
            {
                "name": "Atadi",
                "totalCycleTime": 59.225,
                "totalCost": 4.378,
                "unitCost": [
                    {
                        "lane": "Customer Service Department",
                        "cost": 0.08
                    },
                    {
                        "lane": "Finance Department",
                        "cost": 0.08
                    }
                ],
                "transparency": [
                    {
                        "view": "Customer Service Department View",
                        "numberOfExplicitTask": 4,
                        "transparency": 0.333
                    },
                    {
                        "view": "Finance Department View",
                        "numberOfExplicitTask": 3,
                        "transparency": 0.25
                    },
                    {
                        "view": "Customer View",
                        "numberOfExplicitTask": 5,
                        "transparency": 0.417
                    }
                ],
                "totalNumberExplicitTasks": 12,
                "quality": 0.76,
                "numberOfOptionalTasks": 2,
                "totalTasks": 12,
                "flexibility": 0.166,
                "handledTasks": 0,
                "unHandledTasks": 0,
                "exceptionHandling": 1
            }
        ]

        return JsonResponse(result, safe=False)

    @ staticmethod
    @ api_view(['GET'])
    def evaluate3(request):
        result = [
            {
                "name": "Atadi",
                "totalCycleTime": 73.9,
                "totalCost": 5.921,
                "unitCost": [
                    {
                        "lane": "Customer Service Department",
                        "cost": 0.08
                    },
                    {
                        "lane": "Finance Department",
                        "cost": 0.08
                    }
                ],
                "transparency": [
                    {
                        "view": "Customer Service Department View",
                        "numberOfExplicitTask": 4,
                        "transparency": 0.4
                    },
                    {
                        "view": "Finance Department View",
                        "numberOfExplicitTask": 3,
                        "transparency": 0.3
                    },
                    {
                        "view": "Customer View",
                        "numberOfExplicitTask": 3,
                        "transparency": 0.3
                    }
                ],
                "totalNumberExplicitTasks": 10,
                "quality": 0.2,
                "numberOfOptionalTasks": 8,
                "totalTasks": 10,
                "flexibility": 0.8,

                "handledTasks": 0,
                "unHandledTasks": 0,
                "exceptionHandling": 1
            }
        ]

        return JsonResponse(result, safe=False)

    @ staticmethod
    @ api_view(['GET'])
    def evaluate4(request):
        result = [
            {
                "name": "Atadi",
                "totalCycleTime": 32.5,
                "totalCost": 2.6,
                "unitCost": [
                    {
                        "lane": "Customer Service Department",
                        "cost": 0.08
                    },
                    {
                        "lane": "Finance Department",
                        "cost": 0.08
                    }
                ],
                "transparency": [
                    {
                        "view": "Customer Service Department View",
                        "numberOfExplicitTask": 4,
                        "transparency": 0.445
                    },
                    {
                        "view": "Finance Department View",
                        "numberOfExplicitTask": 2,
                        "transparency": 0.222
                    },
                    {
                        "view": "Customer View",
                        "numberOfExplicitTask": 3,
                        "transparency": 0.333
                    }
                ],
                "totalNumberExplicitTasks": 9,
                "quality": 0.7,
                "numberOfOptionalTasks": 7,
                "totalTasks": 9,
                "flexibility": 0.777,
                "handledTasks": 0,
                "unHandledTasks": 0,
                "exceptionHandling": 1
            }
        ]

        return JsonResponse(result, safe=False)
